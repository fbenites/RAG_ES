import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'RAG_ES')))


from RAG_ES.document_manager import ESConnector
import unittest

class TestESConnectorIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize ESConnector with your Elasticsearch instance details
        cls.connector = ESConnector(host='localhost', port=9200)
        # You might want to create a test index or use a unique index name to avoid data conflicts
        cls.test_index = "test_documents"

    @classmethod
    def tearDownClass(cls):
        # Clean up test data - delete test index
        cls.connector.__es__.indices.delete(index=cls.test_index, ignore=[400, 404])

    def test_store_and_retrieve_document(self):
        # Store a test document
        doc_text = "Integration test document"
        doc_id = self.connector.store_document(doc_text)
        self.assertIsNotNone(doc_id, "Failed to store document")

        # Retrieve the stored document
        retrieved_doc = self.connector.retrieve_document(doc_id)
        self.assertIsNotNone(retrieved_doc, "Document was not found")
        self.assertEqual(retrieved_doc['text'], doc_text, "Retrieved document text does not match stored text")

    def test_search_document(self):
        # Store a document to be searched
        doc_text = "Unique search test document"
        self.connector.store_document(doc_text)

        # Search for the document
        search_response = self.connector.search({"query": {"match": {"text": "Unique search"}}})
        hits = search_response['hits']['hits']
        self.assertGreater(len(hits), 0, "No documents found")
        self.assertIn(doc_text, [hit['_source']['text'] for hit in hits], "Stored document was not found by search")



class TestESConnector(unittest.TestCase):
    @patch('RAG_ES.document_manager.Elasticsearch')
    def test_store_document_success(self, mock_es):
        mock_es.return_value.index.return_value = {'_id': '123'}
        connector = ESConnector()
        doc_id = connector.store_document("Test document")
        self.assertEqual(doc_id, '123')

    @patch('RAG_ES.document_manager.Elasticsearch')
    def test_retrieve_document_found(self, mock_es):
        mock_es.return_value.get.return_value = {'found': True, '_source': 'Test document'}
        connector = ESConnector()
        document = connector.retrieve_document("123")
        self.assertEqual(document, 'Test document')

    @patch('RAG_ES.document_manager.Elasticsearch')
    def test_retrieve_document_not_found(self, mock_es):
        mock_es.return_value.get.return_value = {'found': False}
        connector = ESConnector()
        document = connector.retrieve_document("123")
        self.assertIsNone(document)

    @patch('RAG_ES.document_manager.Elasticsearch')
    def test_search(self, mock_es):
        mock_es.return_value.search.return_value = {'hits': {'hits': [{'_source': 'Test document'}]}}
        connector = ESConnector()
        results = connector.search("Test")
        print(results)
        self.assertEqual(results['hits']['hits'][0]['_source'], 'Test document')

if __name__ == '__main__':
    unittest.main()
