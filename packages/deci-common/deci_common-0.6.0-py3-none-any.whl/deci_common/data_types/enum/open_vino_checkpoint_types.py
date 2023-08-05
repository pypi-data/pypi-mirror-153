from enum import Enum


class OpenVinoCheckpointTypes(str, Enum):
    """
    When passing open vino path to checkpoint, it can be in variant types warping the base xml and bin files.

    Attributes:
    ZIP = zip file contains the xml and bin.
    PICKLE =  pkl file wrapping the xml and bin.
    ORIGIN = xml and bin file.
    """

    ZIP = "zip"
    PICKLE = "pkl"
    XML = "xml"
