import unittest
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'RAG_ES')))

from RAG_ES.llm_summarizer import summarize_with_llm  # Import the function from your script

class SummarizationTest(unittest.TestCase):
    def setUp(self):
        # Any initial setup, like setting up test documents
        self.test_document = "This is a test document to be summarized."

    async def test_single_document_summarization(self):
        summary = await summarize_with_llm([self.test_document])
        self.assertNotEqual(summary, "")
        self.assertIn("summarize", summary)  # Check if the summary reflects the input intention

    def runTest(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.test_single_document_summarization())

if __name__ == '__main__':
    unittest.main()
