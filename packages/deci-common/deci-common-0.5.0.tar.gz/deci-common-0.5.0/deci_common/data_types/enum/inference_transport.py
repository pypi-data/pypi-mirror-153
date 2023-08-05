from enum import Enum


class DataTransportProtocol(str, Enum):
    """
    Enumeration of protocols for inference data transport.
    """

    HTTP = "http"
    IPC = "ipc"
    GRPC = "grpc"
