import os
import sys
from typing import List, Dict

from .document_ingestion import load_documents_from_directory
from .embedding_module import get_embeddings
from .vector_db_module import VectorDB

class RAGPipeline:
    def __init__(self, embedding_dimension: int = 384): # Default dimension for paraphrase-multilingual-MiniLM-L12-v2
        self.vector_db = VectorDB(dimension=embedding_dimension)

    def ingest_documents(self, directory_path: str):
        """
        Loads documents from a directory, chunks them, generates embeddings,
        and adds them to the vector database.
        """
        print(f"Starting document ingestion from: {directory_path}")
        chunks = load_documents_from_directory(directory_path)
        
        if not chunks:
            print("No documents or chunks generated. Skipping embedding and vector DB population.")
            return

        print(f"Generated {len(chunks)} chunks. Generating embeddings...")
        embeddings = get_embeddings(chunks)
        
        # Prepare metadatas for each chunk
        # In a real application, you'd want more robust metadata (e.g., source file, page number)
        metadatas = [{"text": chunk, "chunk_id": i} for i, chunk in enumerate(chunks)]

        self.vector_db.add_vectors(embeddings, metadatas)
        print("Document ingestion complete.")

    def retrieve_information(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieves relevant information from the vector database based on a query.
        """
        print(f"Retrieving information for query: '{query}'")
        query_embedding = get_embeddings([query])[0]
        search_results = self.vector_db.search(query_embedding, k=k)
        return search_results

if __name__ == "__main__":
    # Example usage of the RAG Pipeline
    rag_pipeline = RAGPipeline()

    # Create a dummy directory and some text files for testing
    test_dir = "test_rag_documents"
    os.makedirs(test_dir, exist_ok=True)

    with open(os.path.join(test_dir, "science_facts.txt"), "w", encoding="utf-8") as f:
        f.write("The Earth is the third planet from the Sun. It is the only astronomical object known to harbor life. " * 5 +
                "The speed of light in a vacuum is approximately 299,792,458 meters per second. " * 5)

    with open(os.path.join(test_dir, "history_events.txt"), "w", encoding="utf-8") as f:
        f.write("World War II was a global war that lasted from 1939 to 1945. It involved the vast majority of the world's countries. " * 5 +
                "The fall of the Berlin Wall in 1989 symbolized the end of the Cold War. " * 5)

    # Ingest documents
    rag_pipeline.ingest_documents(test_dir)

    # Perform some queries
    query1 = "Tell me about the Earth."
    results1 = rag_pipeline.retrieve_information(query1, k=2)
    print(f"\nResults for query: '{query1}'")
    for i, result in enumerate(results1):
        print(f"--- Result {i+1} (Distance: {result['distance']:.4f}) ---")
        print(f"Text: {result['metadata']['text']}")

    query2 = "When did the Cold War end?"
    results2 = rag_pipeline.retrieve_information(query2, k=2)
    print(f"\nResults for query: '{query2}'")
    for i, result in enumerate(results2):
        print(f"--- Result {i+1} (Distance: {result['distance']:.4f}) ---")
        print(f"Text: {result['metadata']['text']}")
    
    # Clean up dummy directory
    import shutil
    shutil.rmtree(test_dir)
