from typing import Dict, Any
from copy import deepcopy
from enum import Enum

from deci_common.abstractions.base_model import Schema


class ErrorLevel(str, Enum):
    ERROR = "Error"
    WARNING = "Warning"


class ModelErrorRecord(Schema):
    """
    Serialized model error record. This is intended as an external interface to notify users of problems
        with models uploaded to their lab. The errors list is returned from get_model apis.
    """

    error_type: str
    level: ErrorLevel = ErrorLevel.ERROR
    params: Dict[str, Any]
    message: str = ""


class BaseModelError(Exception):
    """
    Base class for model errors. All errors derived from this class will be logged by deci's job workers
        as a ModelErrorRecord in the model's errors list.

    Note: the cause list for the error is iterated over, so it's Ok to `raise Exception(...) from ex`. The
        error that will be logged will be the first error inheriting from BaseModelError.
    Note: if no BaseModelError is found in the cause chain, the error is converted into ModelInternalError.
    Note: the magic happens in ModelErrorsInterface.
    """

    def __init__(self, user_friendly_message: str, **kwargs):
        super().__init__(user_friendly_message)
        self._user_friendly_message = user_friendly_message

    def encode_error_record(self, level: ErrorLevel = ErrorLevel.ERROR):
        error_type = type(self).__name__
        message = self._user_friendly_message
        params = deepcopy(self.__dict__)
        del params["_user_friendly_message"]
        return ModelErrorRecord(error_type=error_type, params=params, message=message, level=level)


class ModelInternalError(BaseModelError):
    """
    Internal error type for model errors. This will be logged in case an unhandled exception fails one of deci's
        job workers, but no BaseModelError exception was found in the cause chain.
    """

    def __init__(self):
        user_friendly_message = "An internal error occured with the given model. Please contact Deci support."
        super().__init__(user_friendly_message)


class ModelInputDimsMismatchError(BaseModelError):
    def __init__(self, user_input_dims, model_input_dims):
        user_friendly_message = (
            "Failed to benchmark the model using the user-provided input dimensions, "
            "which are different than the dimensions expected by the model."
        )
        super().__init__(user_friendly_message)
        self.user_input_dims = user_input_dims
        self.model_input_dims = model_input_dims


class InvalidInputDimensionsError(BaseModelError):
    def __init__(self, user_input_dims, model_input_dims):
        user_friendly_message = (
            "The model has invalid input dimensions. Please edit the model and provide non-"
            "dynamic input dimensions (positive integers)"
        )
        super().__init__(user_friendly_message)
        self.user_input_dims = user_input_dims
        self.model_input_dims = model_input_dims


class UnsupportedStaticBatchSizeError(BaseModelError):
    def __init__(self, static_batch_size):
        user_friendly_message = (
            f"Failed to benchmark the model using a static batch size of {static_batch_size} which is not yet supported."
            f" Please try to upload a model with dynamic batch size."
        )
        super().__init__(user_friendly_message)
        self.static_batch_size = static_batch_size


class PrimaryBatchSizeAndStaticBatchSizeConflictError(BaseModelError):
    def __init__(self, static_batch_size, primary_batch_size):
        user_friendly_message = (
            "Benchmark process could not be resolved for the requested primary batch size because the model is set to different static batch size."
            "Please try to upload a model with dynamic batch size."
        )
        super().__init__(user_friendly_message)
        self.static_batch_size = static_batch_size
        self.primary_batch_size = primary_batch_size


class BadModelFileReason(str, Enum):
    CORRUPTED_ZIP_FILE = "Failed to unzip the uploaded zip file. Is the file corrupted?"
    BAD_SAVED_MODEL_ZIP = "The provided zip file doesn't contain a valid tensorflow2 saved model."


class BadModelFileError(BaseModelError):
    def __init__(self, reason: BadModelFileReason, **extras):
        user_friendly_message = reason.value
        super().__init__(user_friendly_message)

        self.reason = reason.name
        for param_name, param_value in extras.values():
            setattr(self, param_name, param_value)
