from elasticsearch import Elasticsearch, ElasticsearchException
import logging

def initialize_elasticsearch(host: str = 'localhost', port: int = 9200) -> Elasticsearch:
    """
    Initialize an Elasticsearch client connection.
    """
    try:
        es = Elasticsearch([{'host': host, 'port': port, 'scheme':'http'}])
        if not es.ping():
            raise ValueError("Connection to Elasticsearch failed. Could not ping the Elasticsearch instance.")
        logging.info("Successfully connected to Elasticsearch")
        return es
    except ElasticsearchException as es_exception:
        logging.error(f"Error connecting to Elasticsearch: {es_exception}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while initializing Elasticsearch: {e}", exc_info=True)
        raise

# Example usage (This would typically be called from somewhere else in the application)
es_client = initialize_elasticsearch('localhost', 9200)  # INPUT_REQUIRED {Please replace 'localhost' and '9200' with your Elasticsearch host and port}