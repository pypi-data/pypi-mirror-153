from os import path

from assembly_client.api.types.function_type import SymbiontFunctionType
from assembly_client.api.util.time import utc_time_iso

EVENT_NAMESPACE = "assembly"
GENERIC_EVENT_TYPE_SUFFIX = "deprecated-generic"


class BaseEvent:
    type = ""

    def __init__(self, call_op, data=None):
        self.job_id = call_op.job_id
        self.channel = (
            call_op.tx.write_channel
            if call_op.function_type == SymbiontFunctionType.executable
            else None
        )
        self.signing_key_alias = call_op.key_alias
        self.tx_index = call_op.tx_index
        self.tx_minor_index = call_op.minor_tx_index
        self.data = data

        self.timestamp = utc_time_iso()

    def to_json(self):
        return {
            "type": getattr(self, "type", self.__class__.type),
            "timestamp": self.timestamp,
            "job_id": self.job_id,
            "channel": self.channel,
            "signing_key_alias": self.signing_key_alias,
            "tx_index": self.tx_index,
            "tx_minor_index": self.tx_minor_index,
            "data": self.data,
        }


class ContractEvent(BaseEvent):
    def __init__(self, call_op, type_suffix, data=None):
        self.type = path.join(
            call_op.contract_ref.name, call_op.contract_ref.version, type_suffix
        )
        super().__init__(call_op, data)


class GenericEvent(ContractEvent):
    def __init__(self, call_op, data=None):
        super().__init__(call_op, GENERIC_EVENT_TYPE_SUFFIX, data)


class JobStartEvent(BaseEvent):
    type = path.join(EVENT_NAMESPACE, "job_start")

    def __init__(self, call_op):
        super().__init__(call_op)


class JobCompleteEvent(BaseEvent):
    type = path.join(EVENT_NAMESPACE, "job_complete")

    def __init__(self, call_op, value, key="result"):
        self.value = value
        super().__init__(call_op, data={key: self.value})


class JobFailEvent(BaseEvent):
    type = path.join(EVENT_NAMESPACE, "job_fail")

    def __init__(self, call_op, error):
        self.value = error
        super().__init__(call_op, data={"error": error.to_json()})
