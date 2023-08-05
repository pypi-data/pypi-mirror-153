from abc import ABCMeta
from typing import Any, List, Union

import numpy as np


class AbstractTensorSerializer(ABCMeta):
    """
    Serializes and Deserializes arbitrary data.
    """

    @staticmethod
    def serialize(obj: Union[np.ndarray, List[np.ndarray]]) -> Any:
        """Converts the object to a buffer, which can be later reconstructed using the class's deseralize() method."""
        raise NotImplementedError

    @staticmethod
    def deserialize(obj: Any) -> List[np.ndarray]:
        """
        Deserialized the bytes into a python object.
        """
        raise NotImplementedError
