import os
from document_manager import store_document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_txt_documents(directory_path):
    """
    Load text documents from a specified directory and store them in Elasticsearch.
    
    :param directory_path: Path to the directory containing .txt files.
    """
    if not os.path.isdir(directory_path):
        logging.error(f"The specified directory does not exist: {directory_path}")
        print("no dir")
        return

    for (root,dirs,files)  in os.walk(directory_path):
        for filename in files:            
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)
                print(file_path)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text_content = file.read()
                        print("len",len(text_content))
                        document_id = store_document(text_content)
                        logging.info(f"Document stored successfully with ID: {document_id} from file: {filename}")
                        print(document_id)
                except Exception as e:
                    logging.error(f"Failed to load document from file: {filename}. Error: {e}", exc_info=True)

if __name__ == "__main__":
    import sys
    directory_path = "./data"  # INPUT_REQUIRED {Please replace <directory_path> with the path to your directory containing .txt files}
    load_txt_documents(directory_path)