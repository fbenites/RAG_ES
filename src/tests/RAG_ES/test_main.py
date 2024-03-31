from fastapi.testclient import TestClient
from your_app_file import app  # Import your FastAPI app
import pytest

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Squirro service is running"}

def test_create_document():
    document_data = {"text": "Sample document text"}
    response = client.post("/documents", json=document_data)
    assert response.status_code == 200  # Or the status code you expect
    assert "document_id" in response.json()

def test_get_document():
    # Assuming you have a document with ID "test_id" in your test database
    response = client.get("/documents/test_id")
    assert response.status_code == 200  # Or 404 if not found
    # Further assertions can be made based on the expected response content

def test_search_documents_without_summarize():
    response = client.get("/search?q=squirro")
    assert response.status_code == 200
    # Assertions about the content of the response
    

#Negative tests
def test_search_documents_without_summarize():
    response = client.get("/search?q=squirrol")
    assert response.status_code == 200
    # Assertions about the content of the response


def test_search_documents_with_summarize():
    response = client.get("/search?q=squirro&summarize=true")
    assert response.status_code == 200
    # Assertions about the content of the response, including summarized text
