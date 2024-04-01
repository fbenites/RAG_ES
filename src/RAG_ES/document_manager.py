import logging
from elasticsearch import Elasticsearch


class ESConnector:
    """ Class for wraping the ES client, so we can
    define interfaces to cleanly interact and monitor the singleton"""
    # Configuration for Elasticsearch connection
    
    def __init__(self, host: str = 'localhost', port: int = 9200) -> Elasticsearch:
        """
        Initialize an Elasticsearch client connection.
        """
        try:
            es = Elasticsearch([{'host': host, 'port': port, "scheme": "http"}])
            if not es.ping():
                raise ValueError("Connection to Elasticsearch failed. Could not" 
                                 "ping the Elasticsearch instance.")
            logging.info("Successfully connected to Elasticsearch")
            self.__es__ = es
            self.__index__ = "documents"

        except Exception as e:
            logging.error(f"An unexpected error occurred while"
                          "initializing Elasticsearch: {e}", exc_info=True)
            raise



    def store_document(self, text: str):
        """
        Store a document in Elasticsearch and return the generated document ID.
        """
        try:
            response = self.__es__.index(index=self.__index__, body={"text": text})
            document_id = response['_id']
            logging.info(f"Document stored successfully with ID: {document_id}")
            return document_id
        except Exception as e:
            logging.error(f"Error storing document in Elasticsearch: {e}", exc_info=True)
            raise

    def retrieve_document(self, document_id: str):
        """
        Retrieve a document from Elasticsearch using the document ID.
        """
        try:
            response = self.__es__.get(index=self.__index__, id=document_id)
            if response['found']:
                logging.info(f"Document retrieved successfully with ID: {document_id}")
                return response['_source']
            else:
                logging.info(f"Document not found with ID: {document_id}")
                return None
        except Exception as e:
            logging.error(f"Error retrieving document from Elasticsearch: {e}", exc_info=True)
            raise

    def search(self, body: dict, index: str = None) -> dict:
        """ Interface for searching can be used to check parameters"""
        if index == None:
            return self.__es__.search(body)
        else:
            return self.__es__.search(index=index, body=body)

