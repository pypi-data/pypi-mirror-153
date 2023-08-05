from typing import Optional

from deci_common.abstractions.base_model import Schema
from deci_common.data_types.enum.hardware_enums import (
    HardwareType,
    InferenceHardware,
    MapHardwareTypeToFamily,
    HardwareEnvironment,
    HardwareVendor,
    HardwareLabel,
    HardwareTaint,
    MapHardwareTypeToVendor,
    HardwareMachineModel,
    MapHardwareTypeToEnvironment,
    HardwareImageDistribution,
    HardwareImageRepository,
    MapHardwareTypeToImageDistribution,
    MapHardwareTypeToImageRepository,
)


# TODO move all hardwaretype usage to use thic class insted.
class HardwareReturnSchema(Schema):
    """
    A logic schema of hardware
    """

    name: HardwareType
    vendor: HardwareVendor
    machine: HardwareMachineModel = None


class Hardware(Schema):
    """
    A logic schema of hardware
    """

    name: HardwareType
    type: InferenceHardware
    # equals None for backwards compatibility of benchmark jobs who does not have it.
    machine: HardwareMachineModel = None
    cost_per_hour: int = 0
    environment: HardwareEnvironment
    vendor: HardwareVendor
    label: HardwareLabel
    taint: HardwareTaint
    image_repository: Optional[HardwareImageRepository]
    image_distribution: Optional[HardwareImageDistribution]


def get_hardware_by_hardware_name(hw_name: HardwareType) -> Hardware:
    if type(hw_name) is str:
        hw_name = HardwareType(hw_name)
    hardware_type = MapHardwareTypeToFamily[hw_name.name].value
    image_repository = getattr(MapHardwareTypeToImageRepository, hw_name.name, None)
    image_distribution = getattr(MapHardwareTypeToImageDistribution, hw_name.name, None)
    return Hardware(
        name=hw_name,
        type=hardware_type,
        environment=MapHardwareTypeToEnvironment[hw_name.name].value,
        taint=HardwareTaint[hw_name.name].value,
        machine=HardwareMachineModel[hw_name.name].value,
        vendor=HardwareVendor.INTEL if hardware_type == "cpu" else HardwareVendor.NVIDIA,
        label=HardwareLabel[hw_name.name].value,
        image_repository=image_repository.value if image_repository is not None else None,
        image_distribution=image_distribution.value if image_distribution is not None else None,
    )


def get_hardware_return_schema(hw_name: HardwareType) -> HardwareReturnSchema:
    if type(hw_name) is str:
        hw_name = HardwareType(hw_name)
    return HardwareReturnSchema(
        name=hw_name,
        vendor=MapHardwareTypeToVendor[hw_name.name].value,
        machine=HardwareMachineModel[hw_name.name].value,
    )
