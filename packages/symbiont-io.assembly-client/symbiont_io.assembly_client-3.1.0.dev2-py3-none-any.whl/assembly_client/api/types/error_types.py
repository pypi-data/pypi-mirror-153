import logging

logger = logging.getLogger(__name__)

CONTRACT_REQUEST_SERVER_ERROR = "ContractRequestServerError"


class BaseError(Exception):
    def __init__(self, code, error_type, message, inner=None):
        self.message = message
        self.inner = inner
        self.code = code
        self.error_type = error_type

    def log(self):
        logger.warning(str(self))

    def log_error(self):
        logger.error(str(self))

    def to_json(self):
        return {
            "code": self.code,
            "type": self.error_type,
            "message": self.message,
            "data": str(self.inner)
            if isinstance(self.inner, Exception)
            else self.inner,
        }


class VmError(BaseError):
    def __str__(self):
        messages = [
            self.__class__.__name__,
            "Message: {}".format(self.message),
            "Inner Exception: {}".format(self.inner),
        ]
        if self.inner is not None and hasattr(self.inner, "__traceback__"):
            tb = traceback.extract_tb(self.inner.__traceback__)
            if tb:
                messages.append("traceback: {}".format(str(tb)))

        return "\n".join(messages)


class BaseContractError(VmError):
    """execution time error, type thrown by user code"""

    def __init__(self, message, inner=None):
        status_code = 500
        # determine the class that is extending BaseContractError to figure out the status code
        # this avoids changing the errors_type module in every language version
        sub_class_name = getattr(getattr(self, "__class__", None), "__name__", None)
        if sub_class_name == "ContractError":
            status_code = 400

        super().__init__(
            status_code, CONTRACT_REQUEST_SERVER_ERROR, f"{message}", inner=inner
        )


class ContractError(BaseContractError):
    """execution time error, type thrown by user code"""

    def __init__(self, message, inner=None):
        super().__init__(message, inner=inner)


class ContractImplementationError(ContractError):
    """for any errors determined to be independent of inputs, static bugs"""


class ContractNotFoundError(VmError):
    """for when the contract is not found in the database"""

    def __init__(self, contract_ref):
        super().__init__(
            404, type(self).__name__, "no such contract: '{}'".format(contract_ref)
        )


class ContractFunctionNotFoundError(VmError):
    """for when the specified function does not exist on the contract"""

    def __init__(self, contract_ref, function_name):
        super().__init__(
            404,
            type(self).__name__,
            "no such contract function: '{}.{}'".format(contract_ref, function_name),
        )


class DuplicatePublishError(VmError):
    """for when a user publishes the same contract a second time"""

    def __init__(self, contract_ref):
        super().__init__(
            404,
            type(self).__name__,
            "attempted publish but contract already published: '{}'".format(
                contract_ref
            ),
        )


class KeyAliasNotFoundError(VmError):
    def __init__(self, key_alias):
        super().__init__(
            404, type(self).__name__, "no such key alias: '{}'".format(key_alias)
        )


class LanguageVersionNotAllowed(VmError):
    def __init__(self, tx_index, language_version, language_versions):
        super().__init__(
            404,
            type(self).__name__,
            "As of transaction {}, language version {} is not one of the allowed versions: {}.".format(
                tx_index, language_version, language_versions
            ),
        )


class PublishContractsError(VmError):
    def __init__(self, contract_ref_error_pairs):
        super().__init__(
            400,
            type(self).__name__,
            "some or all contracts are invalid and failed to publish",
            inner=[
                {"ref": contract_ref.to_json(), "error": str(error)}
                for (contract_ref, error) in contract_ref_error_pairs
            ],
        )


class UnrecoverableVmError(ContractError):
    """errors where we cannot recover"""

    def log(self):
        logger.error(str(self))
