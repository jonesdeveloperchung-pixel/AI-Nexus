from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np
import os
import sys

from .document_ingestion import load_documents_from_directory, chunk_text, read_text_file

# Initialize the SentenceTransformer model
# Using a common multilingual model for demonstration
# This model will be downloaded the first time it's used.
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def get_embeddings(texts: List[str]) -> np.ndarray:
    """
    Generates embeddings for a list of text strings.
    """
    if not texts:
        # Return an empty 2D array with the correct embedding dimension
        return np.empty((0, model.get_sentence_embedding_dimension()))
    embeddings = model.encode(texts, convert_to_tensor=False)
    return embeddings

if __name__ == "__main__":
    # Example usage:
    # Create a dummy directory and some text files for testing
    test_dir = "test_documents_for_embeddings"
    os.makedirs(test_dir, exist_ok=True)

    with open(os.path.join(test_dir, "doc1.txt"), "w", encoding="utf-8") as f:
        f.write("This is a sentence about cats. " * 10)

    with open(os.path.join(test_dir, "doc2.txt"), "w", encoding="utf-8") as f:
        f.write("This is a sentence about dogs. " * 10)

    print(f"Loading documents from '{test_dir}' for embedding...")
    # Using load_documents_from_directory to get chunks
    chunks = load_documents_from_directory(test_dir)

    if chunks:
        print(f"Generated {len(chunks)} chunks. Generating embeddings...")
        embeddings = get_embeddings(chunks)
        print(f"Generated embeddings with shape: {embeddings.shape}")
        print("\nFirst embedding (first 5 dimensions):")
        print(embeddings[0][:5])
    else:
        print("No chunks generated to embed.")
    
    # Clean up dummy directory
    import shutil
    shutil.rmtree(test_dir)