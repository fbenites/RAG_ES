from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import logging
from document_manager import store_document, retrieve_document, es
#from elasticsearch.exceptions import ElasticsearchException
from search_reranker import SearchResultReranker
import asyncio
from llm_summarizer import summarize_with_llm

app = FastAPI()

logging.basicConfig(level=logging.INFO)

class Document(BaseModel):
    text: str

# Initialize the SearchResultReranker
search_reranker = SearchResultReranker()

@app.get("/")
async def root():
    logging.info("Root endpoint called")
    try:
        return {"message": "Squirro service is running"}
    except Exception as e:
        logging.error("Error at root endpoint: %s", e, exc_info=True)
        return {"error": "An error occurred"}

@app.post("/documents")
async def create_document(document: Document):
    logging.info("Document creation endpoint called")
    try:
        document_id = store_document(document.text)
        logging.info(f"Document stored successfully with ID: {document_id}")
        return {"document_id": document_id}
    except Exception as e:
        logging.error(f"Failed to store document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to store document")

@app.get("/documents/{document_id}")
async def get_document(document_id: str):
    logging.info(f"Retrieve document endpoint called with ID: {document_id}")
    try:
        document = retrieve_document(document_id)
        if document is not None:
            logging.info(f"Document retrieved successfully with ID: {document_id}")
            return document
        else:
            logging.error(f"Document not found with ID: {document_id}")
            raise HTTPException(status_code=404, detail=f"Document not found with ID: {document_id}")
    except Exception as e:
        logging.error(f"Failed to retrieve document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve document")

@app.get("/search")
async def search_documents(q: str = Query(None, min_length=3, max_length=100), summarize: bool = False):
    logging.info(f"Search endpoint called with query: {q}, summarize: {summarize}")
    try:
        search_results = es.search(index="documents", body={"query": {"match": {"text": q}}})
        hits = search_results['hits']['hits']
        results = [{"document_id": hit["_id"], "text_snippet": hit["_source"]["text"][:100]} for hit in hits]

        if summarize:
            texts_to_summarize = [hit["_source"]["text"] for hit in hits]
            summarized_text = await summarize_with_llm(texts_to_summarize)
            if summarized_text == "An error occurred while summarizing the documents.":
                logging.error("Summarization failed due to an internal error.")
                return {"results": results, "warning": "Failed to summarize documents, returning original search results."}
            logging.info("Summarization completed successfully.")
            # Re-rank the summarized results using the SearchResultReranker
            reranked_summarized_results = search_reranker.rerank(q, [{"document_id": "summarized", "text_snippet": summarized_text}])
            return {"summarized_text": summarized_text, "reranked_results": reranked_summarized_results}
        else:
            # Re-rank the results using the SearchResultReranker
            reranked_results = search_reranker.rerank(q, results)
            logging.info(f"Found {len(reranked_results)} results after re-ranking")
            return {"results": reranked_results}
    #except ElasticsearchException as es_exc:
    #    logging.error(f"Elasticsearch error during search: {es_exc}", exc_info=True)
    #    raise HTTPException(status_code=500, detail="Elasticsearch error during search")
    except Exception as e:
        logging.error(f"Failed to search documents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to search documents")