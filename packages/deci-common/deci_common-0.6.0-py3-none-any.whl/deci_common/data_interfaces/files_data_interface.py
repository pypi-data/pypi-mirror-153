import os
import gdown  # type: ignore[import]
import socket
import zipfile
import os.path
import tempfile
import urllib.error
from uuid import uuid4
from typing import Any, Optional
from urllib.parse import urlparse
from urllib.request import urlretrieve

# This timeout should be big, because InferenceSimulator run take a long time.
import requests
from cryptography.fernet import Fernet, InvalidToken

from deci_common.data_types.model_errors import BadModelFileError, BadModelFileReason

DOWNLOAD_MODEL_TIMEOUT_SECONDS = 5 * 60


class FileDownloadFailedException(Exception):
    pass


class FileCreationFailedException(Exception):
    pass


class FileIsNotEncryptedError(Exception):
    pass


class FilesDataInterface:
    @staticmethod
    def add_directory_to_archive(zipf: zipfile.ZipFile, path: str, zip_root: str = ".") -> None:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_full_path = os.path.join(root, file)
                zip_root_path = os.path.join(path, zip_root)
                relative_path_from_zip_root = os.path.relpath(file_full_path, zip_root_path)
                zipf.write(filename=file_full_path, arcname=relative_path_from_zip_root)

    @staticmethod
    def archive_directory(path: str, archive_path: str, zip_root: str = "../../../deci-common/deci_common") -> str:
        zipf = zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED)
        FilesDataInterface.add_directory_to_archive(zipf=zipf, path=path, zip_root=zip_root)
        zipf.close()

        return archive_path

    @staticmethod
    def download_file_to_memory(file_url: str) -> Any:
        """
        Download a File.
        Args:
            file_url (): The url to download file from

        Returns:
            str contains the binary memory file
        """
        req_for_file = requests.get(file_url, stream=True)
        file_object_from_req = req_for_file.raw
        file = file_object_from_req.read()
        return file

    @staticmethod
    def create_temporary_file(content: str) -> str:
        try:
            fd, path = tempfile.mkstemp()
            with os.fdopen(fd, "w") as tmp:
                tmp.write(content)
        except Exception as e:
            msg = f"Failed to create temporary file with error {e}"
            raise FileCreationFailedException(msg) from e
        return path

    @staticmethod
    def download_temporary_file(
        file_url: str,
        temp_file_prefix: str = "",
        temp_file_suffix: str = "",
        timeout_seconds: Optional[int] = DOWNLOAD_MODEL_TIMEOUT_SECONDS,
    ) -> str:
        """
        Downloads a file to /tempfile.gettempdir/.

        Args:
        :param file_url: The url to downlaod from
        :param temp_file_prefix: The predix to add to the file in the temporary folder
        :param temp_file_suffix: The suffix to add to the file in the temporary folder
        :param timeout_seconds: The timeout in seconds to pass to urllib.setdefaulttimeout. Pass None for no timeout.
        The default timeout is DOWNLOAD_MODEL_TIMEOUT_SECONDS;
        :return: The file's path.
        :raises: FileDownloadFailedException
        """
        tmp_dir = tempfile.gettempdir()
        file_name = temp_file_prefix + str(uuid4()) + temp_file_suffix
        file_path = tmp_dir + os.path.sep + file_name

        # GET THE URL'S FILE EXTENSION
        parsed_url = urlparse(file_url)
        _, file_extension = os.path.splitext(parsed_url.path)

        if file_extension:
            file_path = file_path + file_extension

        # Proprietary downloads
        if "drive.google.com" in file_url:
            FilesDataInterface._download_google_drive_file(file_url, file_path)
        else:
            if "www.dropbox.com" in file_url:
                # Adding dl=1 for dropbox to download the file raw (without html page)
                if "dl=0" not in file_url:
                    file_url += "?dl=1"
                else:
                    file_url = file_url.replace("dl=0", "dl=1")

            # TODO: Use requests with stream and limit the file size and timeouts.
            socket.setdefaulttimeout(timeout_seconds)
            try:
                urlretrieve(file_url, file_path)
            except urllib.error.ContentTooShortError as ex:
                raise FileDownloadFailedException("File download did not finish correctly " + str(ex))

        return file_path

    @staticmethod
    def save_bytes_to_file(file_bytes: bytes, file_name: Optional[str] = None, mode: str = "wb") -> str:
        """
        Writes a buffer to a local file.
        :param file_bytes: The bytes to write.
        :param file_name: The name of the file to create. Defaults to /tempfile.gettempdir/{uuid4} if not specified.
        :param mode: The write open mode.
        """
        file_name = file_name or tempfile.gettempdir() + os.path.sep + str(uuid4())
        with open(file_name, mode) as new_file:
            new_file.write(file_bytes)
        return file_name

    @staticmethod
    def _download_google_drive_file(google_drive_url: str, destination_file_name: str) -> None:
        """
        Wraps gdown package to download files
        :param google_drive_url: The google drive file url.
        :param destination_file_name: The full path the file to save the google drive file into.
        :return:
        """
        try:
            gdown.download(google_drive_url, destination_file_name, quiet=False)
        except Exception as ex:
            raise FileDownloadFailedException("File download did not finish correctly " + str(ex))

    # FIXME - DECIDE ON THE CLEANUP METHOD - MAKE SURE IT WORKS WELL WITH STATIC METHODS
    # def __del__(self):
    #     """
    #     Cleaning the urls downloaded via urlretrieve (_download_temporary_file)
    #     """
    #     urlcleanup()

    @staticmethod
    def encrypt_file(file: bytes, key: bytes) -> bytes:
        """
        This method get a file and a key and encrypt the file with the key.
        Args:
            file (): file to encrypt - byte stream : open(file,'rb'), or str.encode()
            key (): byte str : Fernet.gen_key()

        Returns:
            str contains the cipher file.
        """
        try:
            # Instantiate the object with your key.
            f = Fernet(key)
            # Pass your bytes type message into encrypt.
            ciphertext = f.encrypt(file)
            return ciphertext
        except Exception as e:
            msg = f"Failed to encrypt file {file!r}, err: {e}"
            raise Exception(msg) from e

    @staticmethod
    def decrypt_file(file: bytes, key: bytes) -> bytes:
        """
        This method get a file and a key and decrypt the file with the key.
        Args:
            file (): file to decrypt - encrypted file: FilesDataInterface.encrypt_file()
            key (): byte str : Fernet.gen_key()
        Returns:
            str contains the cipher file.
        """
        try:
            # Load the private key from a file.
            # Instantiate Fernet on the recip system.
            f = Fernet(key)
            # Decrypt the message.
            cleartext = f.decrypt(file)
            return cleartext
        except (InvalidToken, TypeError) as e:
            raise FileIsNotEncryptedError(f"Failed to decrypt file {file!r}, probably it not encrypted.") from e
        except Exception as e:
            msg = f"Failed to decrypt file {file!r}, err: {e}"
            raise Exception(msg) from e

    @staticmethod
    def unzip_tf2_saved_model_checkpoint_file(tf2_saved_model_checkpoint_file_path: str) -> str:
        """
        Unzip a TF2 Saved Model proto to a temp location
            :param tf2_saved_model_checkpoint_file_path:
            :return: The path to the unzipped saved model directory
        """
        try:
            with zipfile.ZipFile(tf2_saved_model_checkpoint_file_path, "r") as zipObj:
                destination_folder = tempfile.mkdtemp(prefix="tf2_saved_model_checkpoints_")
                zipObj.extractall(destination_folder)
        except Exception as e:
            raise BadModelFileError(reason=BadModelFileReason.CORRUPTED_ZIP_FILE) from e

        # IF UNZIPPED FOLDER CONTAINS ONLY A SINGLE FOLDER, MOVE ALL FILES INTO THE UNZIP FOLDER (IN CASE
        # THE ZIP FILE CONTAINED A SINGLE FOLDER)
        if len(os.listdir(destination_folder)) == 1 and os.path.isdir(
            os.path.join(destination_folder, os.listdir(destination_folder)[0])
        ):
            internal_dir = os.path.join(destination_folder, os.listdir(destination_folder)[0])
            for f in os.listdir(internal_dir):
                os.rename(os.path.join(internal_dir, f), os.path.join(destination_folder, f))
            os.removedirs(internal_dir)

        return str(destination_folder)
