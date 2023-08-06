import hashlib
import hmac
from dataclasses import dataclass
from json import JSONDecodeError, dumps, loads
from logging import getLogger
from typing import Any, List, Literal, Optional, Tuple, Union

from jsonpath_ng.ext import parse
from jsonpath_ng.jsonpath import DatumInContext, JSONPath
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.util.types import AttributeValue

from helios.base.span_attributes import SpanAttributes

_LOG = getLogger(__name__)
DATA_TO_DROP = [SpanAttributes.HTTP_RESPONSE_BODY]
DATA_TO_OBFUSCATE = [
    SpanAttributes.DB_QUERY_RESULT,
    SpanAttributes.DB_STATEMENT,
    SpanAttributes.HTTP_REQUEST_BODY,
    SpanAttributes.MESSAGING_PAYLOAD,
]
ExpectedValueType = Optional[Union[str, float, int, bool]]
Mode = Optional[Literal['allowlist', 'blocklist']]
Rules = Optional[List[Union[Tuple[str, ExpectedValueType], str]]]


@dataclass
class DataObfuscatorConfiguration:
    hmac_key: str
    mode: Mode
    rules: Rules


class DataObfuscator:
    _hmac_key: str
    _mode: Mode
    _global_rules: List[Tuple[JSONPath, ExpectedValueType]]
    _local_rules: List[JSONPath]

    def __init__(self, data_obfuscator_configuration: DataObfuscatorConfiguration):
        self._hmac_key = data_obfuscator_configuration.hmac_key
        self._mode = data_obfuscator_configuration.mode
        global_rules: List[Tuple[str, ExpectedValueType]] = []
        local_rules: List[str] = []

        if data_obfuscator_configuration.rules is not None:
            for rule in data_obfuscator_configuration.rules:
                if DataObfuscator._is_global_rule(rule):
                    global_rules.append(rule)
                elif isinstance(rule, str):
                    local_rules.append(rule)
                else:
                    _LOG.debug(f'Ignoring invalid rule {rule}.')

        self._global_rules = DataObfuscator._parse_global_rules(global_rules)
        self._local_rules = DataObfuscator._parse_local_rules(local_rules)

    def obfuscate_data(self, span: ReadableSpan) -> None:
        # noinspection PyProtectedMember
        attributes = span._attributes

        if attributes is None:
            return

        for datum_to_drop in DATA_TO_DROP:
            if datum_to_drop in attributes:
                # noinspection PyUnresolvedReferences
                del attributes[datum_to_drop]

        for datum_to_obfuscate in DATA_TO_OBFUSCATE:
            if datum_to_obfuscate in attributes:
                value = attributes[datum_to_obfuscate]
                # noinspection PyUnresolvedReferences
                attributes[datum_to_obfuscate] = self._obfuscate_datum(value)

    @staticmethod
    def hash(key: str, msg: Any, length: int = 8) -> str:
        return hmac.new(key.encode(), str(msg).encode(), hashlib.sha256).hexdigest()[:length]

    @staticmethod
    def _is_global_rule(rule: Tuple[str, ExpectedValueType]) -> bool:
        if isinstance(rule, (list, tuple)) and len(rule) == 2:
            path_expression, expected_value = rule
            is_valid_path_expression = isinstance(path_expression, str)
            is_valid_expected_value = expected_value is None or isinstance(expected_value, (str, float, int, bool))
            return is_valid_path_expression and is_valid_expected_value

        return False

    @staticmethod
    def _parse_global_rules(
            global_rules: List[Tuple[str, ExpectedValueType]]
    ) -> List[Tuple[JSONPath, ExpectedValueType]]:
        parsed_global_rules: List[Tuple[JSONPath, ExpectedValueType]] = []

        for path_expression, expected_value in global_rules:
            try:
                parsed_path_expression = parse(path_expression)
            except Exception as exception:
                _LOG.debug(f'Ignoring invalid path expression {path_expression}.', exception)
                parsed_path_expression = None

            if parsed_path_expression is not None:
                parsed_global_rules.append((parsed_path_expression, expected_value))

        return parsed_global_rules

    @staticmethod
    def _parse_local_rules(local_rules: List[str]) -> List[JSONPath]:
        parsed_local_rules: List[JSONPath] = []

        for path_expression in local_rules:
            try:
                parsed_local_rules.append(parse(path_expression))
            except Exception as exception:
                _LOG.debug(f'Ignoring invalid path expression {path_expression}.', exception)

        return parsed_local_rules

    def _obfuscate_datum(self, value: AttributeValue) -> AttributeValue:
        if isinstance(value, str):
            dict_or_list: Optional[Union[dict, list]]

            try:
                dict_or_list = loads(value)
            except JSONDecodeError:
                dict_or_list = None

            if dict_or_list is not None:
                if self._mode is None or self._mode == 'allowlist':
                    return self._obfuscate_dict_or_list_in_allowlist_mode(value, dict_or_list)
                elif self._mode == 'blocklist':
                    return self._obfuscate_dict_or_list_in_blocklist_mode(dict_or_list)
                else:
                    raise ValueError(f'Unsupported mode {self._mode}.')

        return self._obfuscate_primitive(value)

    def _obfuscate_dict_or_list_in_allowlist_mode(self, value: str, dict_or_list: Union[dict, list]) -> str:
        if self._match_global_rules(dict_or_list):
            return value
        else:
            nodes = self._extract_nodes(dict_or_list)
            obfuscated_dict_or_list = self._obfuscate_object(dict_or_list)
            self._insert_nodes(obfuscated_dict_or_list, nodes, False)
            return dumps(obfuscated_dict_or_list)

    def _obfuscate_dict_or_list_in_blocklist_mode(self, dict_or_list: Union[dict, list]) -> str:
        if self._match_global_rules(dict_or_list):
            obfuscated_dict_or_list = self._obfuscate_object(dict_or_list)
            return dumps(obfuscated_dict_or_list)
        else:
            nodes = self._extract_nodes(dict_or_list)
            self._insert_nodes(dict_or_list, nodes, True)
            return dumps(dict_or_list)

    def _match_global_rules(self, dict_or_list: Union[dict, list]) -> bool:
        for parsed_path_expression, expected_value in self._global_rules:
            try:
                nodes = parsed_path_expression.find(dict_or_list)
            except Exception as exception:
                _LOG.debug(f'Cannot extract nodes of parsed path expression {parsed_path_expression}.', exception)
                nodes = []

            for node in nodes:
                if node.value == expected_value:
                    return True

        return False

    def _extract_nodes(self, dict_or_list: Union[dict, list]) -> List[DatumInContext]:
        nodes: List[DatumInContext] = []

        for parsed_path_expression in self._local_rules:
            try:
                nodes.extend(parsed_path_expression.find(dict_or_list))
            except Exception as exception:
                _LOG.debug(f'Cannot extract nodes of parsed path expression {parsed_path_expression}.', exception)

        return nodes

    def _insert_nodes(
            self, dict_or_list: Union[dict, list], nodes: List[DatumInContext], obfuscate_values: bool
    ) -> None:
        for node in nodes:
            try:
                parse(str(node.full_path)).update(
                    dict_or_list, self._obfuscate_object(node.value) if obfuscate_values else node.value
                )
            except Exception as exception:
                _LOG.debug(f'Cannot insert node {node} into dictionary or list.', exception)

    def _obfuscate_object(self, object_to_obfuscate: Any) -> Any:
        if isinstance(object_to_obfuscate, dict):
            return {key: self._obfuscate_object(value) for key, value in object_to_obfuscate.items()}
        elif isinstance(object_to_obfuscate, list):
            return [self._obfuscate_object(value) for value in object_to_obfuscate]
        else:
            return self._obfuscate_primitive(object_to_obfuscate)

    def _obfuscate_primitive(self, primitive: Any) -> Any:
        if primitive is None or isinstance(primitive, bool):
            return primitive

        try:
            return DataObfuscator.hash(self._hmac_key, primitive)
        except Exception as exception:
            _LOG.debug(f'Cannot hash primitive {primitive}.', exception)
            return '********'
