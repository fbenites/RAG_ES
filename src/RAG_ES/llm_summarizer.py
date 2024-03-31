import logging
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
import asyncio

# Configure logging to include the level, time, and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

model_name = "mistralai/Mistral-7B-Instruct-v0.1"  # INPUT_REQUIRED {Please replace 'TheBloke/Llama-2-7B-Chat-GGUF' with the correct model if different}
logging.info("Loading model and tokenizer.")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, load_in_4bit=True)

async def summarize_with_llm(documents):
    """
    Summarizes a list of documents using a pre-trained LLM ('llama 2 7b (4bit)') model.
    
    :param documents: A list of document strings to be summarized.
    :return: A single string containing the summarized version of the documents.
    """
    try:
        # Load model and tokenizer
        if tokenizer.pad_token is None:
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            model.resize_token_embeddings(len(tokenizer))

        # Concatenate documents
        concatenated_docs = "summarize following documents, DONT overREPEAT: "+" ".join(documents)
        logging.info("Concatenating documents for summarization.")
        inputs = tokenizer(concatenated_docs, return_tensors="pt", truncation=True, padding=True)

        # Check if the tokenized input exceeds the model's max input size
        max_model_input_size = tokenizer.model_max_length
        
        
        if len(inputs["input_ids"][0]) > max_model_input_size:
            logging.info("Input exceeds max model input size, splitting into chunks.")
            # If it does, split the input into chunks based on token count
            input_ids = inputs["input_ids"][0]
            input_chunks = [input_ids[i:i+max_model_input_size] for i in range(0, len(input_ids), max_model_input_size)]
            summaries = []
            for chunk_ids in input_chunks:
                chunk_inputs = {"input_ids": chunk_ids.unsqueeze(0)}  # Add batch dimension
                summary_ids = model.generate(**chunk_inputs, num_beams=4, max_length=200, early_stopping=True)
                summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                summaries.append(summary)
            final_summary = " ".join(summaries)
        else:
            # If not, generate summary directly
            logging.info("Generating summary directly.")
            summary_ids = model.generate(inputs["input_ids"][:1,:500], num_beams=4, max_length=501, early_stopping=True)
            final_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        logging.info("Summary generated successfully.")
        return final_summary
    except Exception as e:
        logging.error(f"Failed to generate summary with LLM: {e}", exc_info=True)
        return "An error occurred while summarizing the documents."
