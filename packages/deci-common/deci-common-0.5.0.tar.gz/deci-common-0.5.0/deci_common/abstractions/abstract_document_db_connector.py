from abc import abstractmethod

from deci_common.abstractions.abstract_logger import ILogger


class AbstractDocumentDBConnector(ILogger):
    """
    Provides operations on document databases.
    """

    @abstractmethod
    def _insert_document(self, document_json: dict):
        raise NotImplementedError()

    @abstractmethod
    def _get_document(self, search_filter: dict) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def _update_document(self, search_filter: dict, updated_document: dict, upsert: bool = False):
        raise NotImplementedError()

    @abstractmethod
    def _update_and_return_document(self, search_filter: dict, updated_document: dict, upsert: bool = False):
        raise NotImplementedError()

    @abstractmethod
    def _delete_document(self, search_filter: dict):
        raise NotImplementedError()
