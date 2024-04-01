# Squirro

Squirro is a cutting-edge HTTP REST service designed for the storage, retrieval, and search of natural language documents. It simplifies the process of finding documents through a free text search feature, akin to Google's search functionality. Additionally, it explores an advanced capability of utilizing a Large Language Model (LLM) to directly generate answers to user queries, offering a more intuitive search experience.

## Overview

The service is engineered using Python, with FastAPI as the web framework for its rapid development capabilities and performance efficiency. Elasticsearch is employed for its powerful document storage and search functionalities, making Squirro a robust solution for managing and querying large volumes of text data. The project structure is straightforward, comprising primary components for document management, search functionality, and an additional module for enhancing search results through re-ranking.

## Features

- Efficient storage and retrieval of documents with unique identifiers.
- Free text search capability for easy document discovery.
- Advanced search enhancements using a Large Language Model for direct answer generation.
- Implementation of REST best practices for a seamless API experience.

## Getting started

### Requirements

- Python 3.9 or later
- FastAPI
- Uvicorn
- Elasticsearch
- transformers library for re-ranking functionality

### Quickstart

1. Ensure Python 3.9 (3.10) and pip are installed on your system.
2. Install the required dependencies using `pip install -r requirements.txt` (virtual enviroment `venv`).
3. Confirm that Elasticsearch is running and accessible.
4. Launch the FastAPI application with `uvicorn main:app --host 0.0.0.0 --port 8000`.
5. Interact with the application through the `/documents` endpoint for storing and retrieving documents, and the `/search` endpoint for document search functionality.

### Loading Documents from Text Files

To load documents from text files into Elasticsearch:

1. Place your text files in a directory of your choice.
2. Run the `load_documents.py` script with the directory path as an argument. Example command:
   ```
   python load_documents.py /path/to/your/text/files
   ```
   This will read each text file in the specified directory, extract the content, and store it as a document in Elasticsearch.

### License

Copyright (c) 2024.