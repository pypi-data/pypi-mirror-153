from opentelemetry.propagators import textmap
from typing import Optional, List
from helios.instrumentation.botocore.consts import AwsParam


class SQSContextGetter(textmap.Getter):
    def get(self, carrier: textmap.CarrierT, key: str) -> Optional[List[str]]:
        if carrier is None:
            return None

        value = carrier.get(key, dict()).get(AwsParam.STRING_VALUE)
        if value is not None:
            return [value]
        return None

    def keys(self, carrier: textmap.CarrierT) -> List[str]:
        if carrier is None:
            return []
        return list(carrier.keys())


class SQSContextSetter(textmap.Setter):
    def set(self, carrier: textmap.CarrierT, key: str, value: str) -> None:
        if carrier is not None and key and value:
            carrier[key] = {
                AwsParam.STRING_VALUE: value,
                AwsParam.DATA_TYPE: 'String'
            }
