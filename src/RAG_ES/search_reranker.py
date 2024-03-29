from transformers import pipeline
import logging

class SearchResultReranker:
    def __init__(self):
        try:
            self.reranker = pipeline("text-classification", model="bert-base-uncased", return_all_scores=True)
            logging.info("BERT model loaded for re-ranking.")
        except Exception as e:
            logging.error("Failed to load BERT model for re-ranking: %s", e, exc_info=True)
            raise

    def rerank(self, query, search_results):
        reranked_results = []
        try:
            for result in search_results:
                input_text = f"query: {query} document: {result['text_snippet']}"
                scores = self.reranker(input_text)[0]
                score = self._extract_relevance_score(scores)
                reranked_results.append((score, result))
            
            # Sort results based on the computed relevance score in descending order
            reranked_results.sort(key=lambda x: x[0], reverse=True)
            
            # Return only the document details after sorting
            return [result for _, result in reranked_results]
        except Exception as e:
            logging.error("Failed to re-rank search results: %s", e, exc_info=True)
            raise

    @staticmethod
    def _extract_relevance_score(scores):
        try:
            # Assuming a binary classification model with labels ['irrelevant', 'relevant']
            for score in scores:
                if score["label"] == "LABEL_1":  # Assuming LABEL_1 is the 'relevant' label
                    return score["score"]
            return 0  # Default to 0 if 'relevant' label score not found
        except Exception as e:
            logging.error("Failed to extract relevance score: %s", e, exc_info=True)
            raise