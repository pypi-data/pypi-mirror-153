import datetime
from abc import ABCMeta
from typing import Type

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from deci_common.abstractions.abstract_document_db_connector import AbstractDocumentDBConnector
from deci_common.data_interfaces.files_data_interface import FilesDataInterface


class MongoDBConfiguration:
    """
    The base of the mongo db configurations - Classes may derive from it and change only the 'COLLECTION'.
    """

    __metaclass__ = ABCMeta

    DATABASE_NAME = None
    HOST = None
    PORT = None
    USERNAME = None
    PASSWORD = None
    AUTH_DB = None  # The database on which will preform the authentication
    COLLECTION = None
    PEM_FILE_URL = None  # The pem file for TLS connection stored inside AWS SecretsManager


class MongoDBConnector(AbstractDocumentDBConnector):
    """
    An abstract MongoDBConnector that operates on a collection (SQL Table equivalent).
    """

    def __init__(self, mongo_db_configuration: Type[MongoDBConfiguration]):
        assert issubclass(mongo_db_configuration, MongoDBConfiguration)
        self._db_config: Type[MongoDBConfiguration] = mongo_db_configuration
        self._client: MongoClient = None
        super().__init__()

    @property
    def client(self) -> MongoClient:
        if not self._client:
            raise RuntimeError('The client is not initialized. You must use the client withing a "with" clause')
        return self._client

    def __create_client(self) -> MongoClient:
        """
        Creates a new pymongo.MongoClient for DB operations.
        """
        client = MongoClient(
            host=self._db_config.HOST,
            port=self._db_config.PORT,
            username=self._db_config.USERNAME,
            password=self._db_config.PASSWORD,
            uuidRepresentation="pythonLegacy",
            retryWrites=False,
            connect=True,
            tls=True,
            tlsCAFile=FilesDataInterface.download_temporary_file(self._db_config.PEM_FILE_URL),
        )
        self._logger.debug("Authenticated to db successfully.")

        return client

    def _get_collection(self, collection_name: str = None) -> Collection:
        """
        Returns a specific collection (NoSQL Equivalent to Table in SQL, by the collection's name. :param
        collection_name: The name of the collection (table) to fetch. Default it the collection from the
        MongoDbConfiguration
        """
        if not collection_name:
            collection_name = self._db_config.COLLECTION
        db = self.client[self._db_config.DATABASE_NAME]
        return db[collection_name]

    def _delete_document(self, search_filter: dict):
        """
        Deletes a document from the collection.
        """
        collection = self._get_collection()
        return collection.delete_one(filter=search_filter)

    def _insert_document(self, document_json: dict):
        now = datetime.datetime.utcnow()
        document_json.update({"creation_time": now, "update_time": now})
        collection = self._get_collection()
        return collection.insert_one(document=document_json)

    def _get_document(self, search_filter: dict) -> dict:
        collection = self._get_collection()
        doc = collection.find_one(filter=search_filter)
        return doc

    def _get_documents(self, search_filter: dict) -> Cursor:
        collection = self._get_collection()
        amount = collection.count_documents(search_filter)
        if not amount:
            return []
        documents_cursor = collection.find(filter=search_filter)
        if documents_cursor:
            return documents_cursor
        return []

    def _update_document(self, search_filter: dict, updated_document: dict, upsert: bool = False):
        updated_document.update({"update_time": datetime.datetime.utcnow()})
        collection = self._get_collection()
        return collection.update_one(filter=search_filter, update={"$set": updated_document}, upsert=upsert)

    def _update_and_return_document(self, search_filter: dict, updated_document: dict, upsert: bool = False):
        updated_document.update({"update_time": datetime.datetime.utcnow()})
        collection = self._get_collection()
        collection.find_one_and_update(filter=search_filter, update={"$set": updated_document}, upsert=upsert)
        return collection.find_one_and_update(filter=search_filter, update={"$set": updated_document}, upsert=upsert)

    def _remove_from_list_and_return_document(self, search_filter: dict, remove_query: dict):
        collection = self._get_collection()
        return collection.find_one_and_update(
            filter=search_filter, update={"$pull": remove_query, "$set": {"update_time": datetime.datetime.utcnow()}}
        )

    def _add_to_list_and_return_document(self, search_filter: dict, add_query: dict):
        collection = self._get_collection()
        return collection.find_one_and_update(
            filter=search_filter,
            update={"$addToSet": add_query, "$set": {"update_time": datetime.datetime.utcnow()}},
            upsert=True,
        )

    def _increment_a_field(self, search_filter: dict, increment_query: dict):
        collection = self._get_collection()
        collection.update_one(
            filter=search_filter,
            update={"$inc": increment_query, "$set": {"update_time": datetime.datetime.utcnow()}},
            upsert=True,
        )

    def __enter__(self):
        if not self._client:
            self._client = self.__create_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # The following lines will close the connection after __exit__, or after each 'with' statement.
        # Disabling this behaviour and keeping the client alive all the time (self._client initialized once).
        # self._client.close()
        # self._client = None
