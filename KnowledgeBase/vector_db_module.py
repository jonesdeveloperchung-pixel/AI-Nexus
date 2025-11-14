import faiss
import numpy as np
from typing import List, Dict
import os
import sys

from .document_ingestion import load_documents_from_directory
from .embedding_module import get_embeddings

class VectorDB:
    def __init__(self, dimension: int):
        """
        Initializes the FAISS index.
        :param dimension: The dimension of the embeddings.
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
        self.metadatas = []  # To store original text chunks and other metadata

    def add_vectors(self, embeddings: np.ndarray, metadatas: List[Dict]):
        """
        Adds embeddings and their associated metadata to the FAISS index.
        :param embeddings: A numpy array of embeddings.
        :param metadatas: A list of dictionaries, where each dictionary contains metadata
                          for the corresponding embedding.
        """
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension mismatch. Expected {self.dimension}, got {embeddings.shape[1]}")
        self.index.add(embeddings)
        self.metadatas.extend(metadatas)
        print(f"Added {len(embeddings)} vectors to the index. Total vectors: {self.index.ntotal}")

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """
        Searches the index with a query embedding and returns the top k most similar items.
        :param query_embedding: A numpy array representing the query embedding.
        :param k: The number of nearest neighbors to retrieve.
        :return: A list of dictionaries, each containing the metadata of a retrieved item.
        """
        if query_embedding.shape[0] != self.dimension:
            raise ValueError(f"Query embedding dimension mismatch. Expected {self.dimension}, got {query_embedding.shape[0]}")
        
        # Reshape query_embedding to be 2D if it's 1D
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:  # FAISS returns -1 for padding if k > ntotal
                continue
            result = {
                "metadata": self.metadatas[idx],
                "distance": distances[0][i]
            }
            results.append(result)
        return results

if __name__ == "__main__":
    # Example usage:
    test_dir = "test_documents_for_vector_db"
    os.makedirs(test_dir, exist_ok=True)

    with open(os.path.join(test_dir, "doc_cat.txt"), "w", encoding="utf-8") as f:
        f.write("Cats are domesticated carnivorous mammals. They are often called house cats when kept as indoor pets. " * 5)

    with open(os.path.join(test_dir, "doc_dog.txt"), "w", encoding="utf-8") as f:
        f.write("Dogs are domesticated mammals, not typically wild animals. They are known for their loyalty and companionship. " * 5)

    with open(os.path.join(test_dir, "doc_bird.txt"), "w", encoding="utf-8") as f:
        f.write("Birds are a group of warm-blooded vertebrates characterized by feathers, toothless beaked jaws, the laying of hard-shelled eggs. " * 5)

    print(f"Loading documents from '{test_dir}'...")
    chunks = load_documents_from_directory(test_dir)

    if chunks:
        print(f"Generated {len(chunks)} chunks. Generating embeddings...")
        embeddings = get_embeddings(chunks)
        
        # Prepare metadatas for each chunk
        metadatas = [{"text": chunk, "source": f"chunk_{i}"} for i, chunk in enumerate(chunks)]

        # Initialize VectorDB
        embedding_dimension = embeddings.shape[1]
        vector_db = VectorDB(dimension=embedding_dimension)

        # Add vectors to the database
        vector_db.add_vectors(embeddings, metadatas)

        # Perform a sample search
        query = "What are common characteristics of pets?"
        print(f"\nSearching for: '{query}'")
        query_embedding = get_embeddings([query])[0]  # Get embedding for the query
        
        search_results = vector_db.search(query_embedding, k=2)

        print("\nSearch Results:")
        for i, result in enumerate(search_results):
            print(f"--- Result {i+1} (Distance: {result['distance']:.4f}) ---")
            print(f"Source: {result['metadata']['source']}")
            print(f"Text: {result['metadata']['text']}")
    else:
        print("No chunks generated to add to vector database.")
    
    # Clean up dummy directory
    import shutil
    shutil.rmtree(test_dir)
