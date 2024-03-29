from elasticsearch import Elasticsearch
#from elasticsearch.exceptions import ElasticsearchException
import logging

def initialize_elasticsearch(host: str = 'localhost', port: int = 9200) -> Elasticsearch:
    """
    Initialize an Elasticsearch client connection.
    """
    try:
        es = Elasticsearch([{'host': host, 'port': port, "scheme": "http"}])
        #if not es.ping():
        #    raise ValueError("Connection to Elasticsearch failed. Could not ping the Elasticsearch instance.")
        logging.info("Successfully connected to Elasticsearch")
        return es
 #   except ElasticsearchException as es_exception:
 #       logging.error(f"Error connecting to Elasticsearch: {es_exception}", exc_info=True)
#        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while initializing Elasticsearch: {e}", exc_info=True)
        raise

es = initialize_elasticsearch('localhost', 9200)

def store_document(text: str):
    """
    Store a document in Elasticsearch and return the generated document ID.
    """
    try:
        response = es.index(index="documents", body={"text": text})
        document_id = response['_id']
        logging.info(f"Document stored successfully with ID: {document_id}")
        return document_id
    except Exception as e:
        logging.error(f"Error storing document in Elasticsearch: {e}", exc_info=True)
        raise

def retrieve_document(document_id: str):
    """
    Retrieve a document from Elasticsearch using the document ID.
    """
    try:
        response = es.get(index="documents", id=document_id)
        if response['found']:
            logging.info(f"Document retrieved successfully with ID: {document_id}")
            return response['_source']
        else:
            logging.info(f"Document not found with ID: {document_id}")
            return None
    except Exception as e:
        logging.error(f"Error retrieving document from Elasticsearch: {e}", exc_info=True)
        raise