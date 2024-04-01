#Elastic Search running on 9200
cd src/RAG_ES
../../.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
