from enum import Enum

# TODO: rename HardwareType to HardwareName and inferenceHardware to HardwareType
from deci_common.data_types.enum.models_enums import BatchSize, BatchSizeEdge
from deci_common.helpers import get_enum_values


class HardwareType(str, Enum):
    """
    The type of the hardware to run on (CPU/GPU Names)
    """

    K80 = "K80"
    V100 = "V100"
    T4 = "T4"
    CPU = "CPU"
    EPYC = "EPYC"
    XAVIER = "Jetson Xavier"
    NANO = "Jetson Nano"
    XAVIER_AGX = "Jetson Xavier AGX"
    CASCADE_LAKE = "Cascade Lake"
    SKYLAKE = "Skylake"
    Broadwell = "Broadwell"
    NUC_TIGER_LAKE = "Intel NUC Tiger Lake"


class HardwareMachineModel(str, Enum):
    K80 = "p2.xlarge"
    V100 = "p3.2xlarge"
    T4 = "g4dn.2xlarge"
    CPU = "c5.4xlarge"
    EPYC = "c5a.2xlarge"
    NANO = "Jetson Nano"
    XAVIER = "Jetson Xavier"
    XAVIER_AGX = "Jetson Xavier AGX"
    CASCADE_LAKE = "c5.4xlarge"
    SKYLAKE = "c5n.4xlarge"
    Broadwell = "m4.4xlarge"
    NUC_TIGER_LAKE = "Intel NUC Tiger Lake"


class InferenceHardware(str, Enum):
    """
    Hardware that can be used for deep learning inference.
    """

    CPU = "cpu"
    GPU = "gpu"


class MapHardwareTypeToFamily(str, Enum):
    # GPUs
    V100 = InferenceHardware.GPU.value
    K80 = InferenceHardware.GPU.value
    T4 = InferenceHardware.GPU.value
    NANO = InferenceHardware.GPU.value
    XAVIER = InferenceHardware.GPU.value
    XAVIER_AGX = InferenceHardware.GPU.value

    # CPUs
    CPU = InferenceHardware.CPU.value
    EPYC = InferenceHardware.CPU.value
    CASCADE_LAKE = InferenceHardware.CPU.value
    SKYLAKE = InferenceHardware.CPU.value
    Broadwell = InferenceHardware.CPU.value
    NUC_TIGER_LAKE = InferenceHardware.CPU.value


class InferyVersion(str, Enum):
    CPU = "cpu"
    GPU = "gpu"
    JETSON = "jetson"


class MapHardwareTypeToInferyVersion(str, Enum):
    # GPUs
    V100 = InferyVersion.GPU.value
    K80 = InferyVersion.GPU.value
    T4 = InferyVersion.GPU.value

    # Jetsons
    NANO = InferyVersion.JETSON.value
    XAVIER = InferyVersion.JETSON.value
    XAVIER_AGX = InferyVersion.JETSON.value

    # CPUs
    CPU = InferyVersion.CPU.value
    EPYC = InferyVersion.CPU.value
    CASCADE_LAKE = InferyVersion.CPU.value
    SKYLAKE = InferyVersion.CPU.value
    Broadwell = InferyVersion.CPU.value
    NUC_TIGER_LAKE = InferyVersion.CPU.value


class HardwareEnvironment(str, Enum):
    GCP = "gcp"
    AWS = "aws"
    Azure = "azure"
    PREMISE = "on premise"


class HardwareVendor(str, Enum):
    INTEL = "intel"
    NVIDIA = "nvidia"
    AMD = "amd"


class HardwareTaint(str, Enum):
    # GPUs
    V100 = "nvidia.com/v100gpu"
    K80 = "nvidia.com/k80gpu"
    T4 = "nvidia.com/t4gpu"
    NANO = "nvidia.com/jetson-nano"
    XAVIER = "nvidia.com/jetson-xavier"
    XAVIER_AGX = "nvidia.com/jetson-xavier-agx"
    # CPUs
    EPYC = "amd.com/epyc"
    CASCADE_LAKE = "intel.com/cascade-lake"
    SKYLAKE = "intel.com/skylake"
    Broadwell = "intel.com/broadwell"
    NUC_TIGER_LAKE = "intel.com/nuc-tiger-lake"


class HardwareLabel(str, Enum):
    # GPUs
    V100 = "nvidia-tesla-v100"
    K80 = "nvidia-tesla-k80"
    T4 = "nvidia-tesla-t4"
    M60 = "nvidia-m60"
    NANO = "nvidia-jetson-nano"
    XAVIER = "nvidia-jetson-xavier"
    XAVIER_AGX = "nvidia-jetson-xavier-agx"

    # CPUs
    EPYC = "amd-epyc"
    CASCADE_LAKE = "intel-cascade-lake"
    SKYLAKE = "intel-skylake"
    Broadwell = "intel-broadwell"
    NUC_TIGER_LAKE = "intel-nuc-tiger-lake"


class MapHardwareTypeToVendor(str, Enum):
    V100 = HardwareVendor.NVIDIA.value
    K80 = HardwareVendor.NVIDIA.value
    T4 = HardwareVendor.NVIDIA.value
    EPYC = HardwareVendor.AMD.value
    NANO = HardwareVendor.NVIDIA.value
    XAVIER = HardwareVendor.NVIDIA.value
    XAVIER_AGX = HardwareVendor.NVIDIA.value
    CASCADE_LAKE = HardwareVendor.INTEL.value
    SKYLAKE = HardwareVendor.INTEL.value
    Broadwell = HardwareVendor.INTEL.value
    NUC_TIGER_LAKE = HardwareVendor.INTEL.value


class MapHardwareTypeToEnvironment(str, Enum):
    # AWS
    V100 = HardwareEnvironment.AWS.value
    K80 = HardwareEnvironment.AWS.value
    T4 = HardwareEnvironment.AWS.value
    EPYC = HardwareEnvironment.AWS.value
    CASCADE_LAKE = HardwareEnvironment.AWS.value
    SKYLAKE = HardwareEnvironment.AWS.value
    Broadwell = HardwareEnvironment.AWS.value

    # PREMISE
    NANO = HardwareEnvironment.PREMISE.value
    XAVIER = HardwareEnvironment.PREMISE.value
    XAVIER_AGX = HardwareEnvironment.PREMISE.value
    NUC_TIGER_LAKE = HardwareEnvironment.PREMISE.value


class MapHardwareTypeToDefaultBatchSizeList(list, Enum):
    V100 = get_enum_values(BatchSize)
    K80 = get_enum_values(BatchSize)
    T4 = get_enum_values(BatchSize)
    EPYC = get_enum_values(BatchSize)
    NANO = get_enum_values(BatchSizeEdge)
    XAVIER = get_enum_values(BatchSizeEdge)
    XAVIER_AGX = get_enum_values(BatchSizeEdge)
    CASCADE_LAKE = get_enum_values(BatchSize)
    SKYLAKE = get_enum_values(BatchSize)
    Broadwell = get_enum_values(BatchSize)
    NUC_TIGER_LAKE = get_enum_values(BatchSize)


class HardwareImageRepository(str, Enum):
    INTEL = "intel"
    JETSON = "jetson"


class MapHardwareTypeToImageRepository(str, Enum):
    NANO = HardwareImageRepository.JETSON.value
    XAVIER = HardwareImageRepository.JETSON.value
    XAVIER_AGX = HardwareImageRepository.JETSON.value
    NUC_TIGER_LAKE = HardwareImageRepository.INTEL.value


class HardwareImageDistribution(str, Enum):
    J46 = "j46"


class MapHardwareTypeToImageDistribution(str, Enum):
    NANO = HardwareImageDistribution.J46.value
    XAVIER = HardwareImageDistribution.J46.value
    XAVIER_AGX = HardwareImageDistribution.J46.value
