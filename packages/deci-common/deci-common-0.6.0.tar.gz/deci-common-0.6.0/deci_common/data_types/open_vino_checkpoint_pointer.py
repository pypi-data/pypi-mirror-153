import magic
from pathlib import Path

from deci_common.abstractions.base_model import Schema
from deci_common.data_types.enum.open_vino_checkpoint_types import OpenVinoCheckpointTypes


class OpenVinoCheckpointTypeResolutionError(Exception):
    pass


class OpenVinoCheckpointPointer(Schema):
    checkpoint_path: str
    type: OpenVinoCheckpointTypes = OpenVinoCheckpointTypes.XML

    @staticmethod
    def get_openvino_checkpoint_pointer_from_path(file_path) -> dict:
        """
        Returns a dict of the checkpoint file path and extension
        :param file_path:
        :return: dict
        """
        try:
            file_path_extension = Path(file_path).suffix

            if file_path_extension:
                # REMOVE THE '.' FROM THE FILE EXTENSION
                file_type_extension = file_path_extension.split(".")[-1]
            else:
                # GET THE FILE TYPE FROM THE BINARY MAGIC NUMBER - WORKS ONLY ON NON-UNIX SYSTEMS
                file_type_extension = OpenVinoCheckpointPointer._infer_openvino_file_type_from_binary(file_path)

            pointer = {"checkpoint_path": file_path, "type": file_type_extension}
            return pointer
        except ValueError as e:
            msg = f"The file type is not supported for open vino {file_path}."
            raise Exception(msg) from e

    @staticmethod
    def _infer_openvino_file_type_from_binary(binary_file_path) -> str:
        """
        Helper method to get the file type from the magic number header of the binary (Works only on Unix)
            -- Requires a local installation of libmagic1 on ubuntu
        :param binary_file_path:
        :return:
        """
        try:
            file_type_magic = magic.from_file(binary_file_path, mime=True)

            if ("xml" in file_type_magic) or ("text/plain" in file_type_magic):
                return OpenVinoCheckpointTypes.XML

            elif "zip" in file_type_magic:
                return OpenVinoCheckpointTypes.ZIP

            elif "octet-stream" in file_type_magic:
                return OpenVinoCheckpointTypes.PICKLE

            else:
                raise OpenVinoCheckpointTypeResolutionError(
                    "Could not infer checkpoint file type from binary magic number for: " + str(file_type_magic)
                )

        except OSError as ex:
            msg = "OpenVino file type resolution is supported only on UNIX systems"
            raise OpenVinoCheckpointTypeResolutionError(msg) from ex
