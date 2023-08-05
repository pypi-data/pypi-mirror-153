from enum import Enum

from deci_common.data_types.enum.hardware_enums import InferenceHardware


class FrameworkFileExtension(Enum):
    TENSORFLOW1 = [".pb"]
    TENSORFLOW2 = [".zip"]
    PYTORCH = [".pth", ".pt"]
    ONNX = [".onnx"]
    TENSORRT = [".pkl"]
    OPENVINO = [".pkl"]
    TORCHSCRIPT = [".pth", ".pt"]
    TVM = None
    KERAS = [".h5"]
    TFLITE = [".tflite"]
    COREML = [".mlmodel"]


class FrameworkType(str, Enum):
    """
    A general deep learning framework, without a version.
    """

    TENSORFLOW1 = "tf1"
    TENSORFLOW2 = "tf2"
    PYTORCH = "pytorch"
    ONNX = "onnx"
    TORCHSCRIPT = "torchscript"
    TENSORRT = "trt"
    TVM = "tvm"
    OPENVINO = "openvino"
    KERAS = "keras"
    TFLITE = "tflite"
    COREML = "coreml"

    @staticmethod
    def from_string(framework: str) -> Enum:
        framework = framework.lower()
        return FrameworkType(framework)


def get_hardware_families_by_framework_type(framework: FrameworkType):
    if framework == FrameworkType.OPENVINO:
        return [InferenceHardware.CPU]
    elif framework == FrameworkType.TENSORRT:
        return [InferenceHardware.GPU]
    else:
        return [InferenceHardware.GPU, InferenceHardware.CPU]
