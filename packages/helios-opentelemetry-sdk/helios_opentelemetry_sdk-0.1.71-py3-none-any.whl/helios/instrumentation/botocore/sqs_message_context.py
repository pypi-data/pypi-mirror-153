
from opentelemetry.context import detach, attach
from opentelemetry.propagate import extract
from helios.instrumentation.botocore.consts import AwsParam
from helios.instrumentation.botocore.utils import SQSContextGetter


class SqsMessageContext:
    def __init__(self, message):
        self.message = message
        self.token = None

    def __enter__(self):
        message_attributes = self.message.get(AwsParam.MESSAGE_ATTRIBUTES, None)
        if message_attributes is None:
            return

        extracted_context = extract(message_attributes, getter=SQSContextGetter())
        self.token = attach(extracted_context)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.token is not None:
            detach(self.token)
