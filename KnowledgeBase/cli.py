import argparse
import os
import sys

from .rag_pipeline import RAGPipeline

def main():
    parser = argparse.ArgumentParser(description="RAG Pipeline CLI for document ingestion and retrieval.")
    parser.add_argument("--doc_dir", type=str, required=True,
                        help="Path to the directory containing documents for ingestion.")
    
    args = parser.parse_args()

    if not os.path.isdir(args.doc_dir):
        print(f"Error: Document directory '{args.doc_dir}' not found or is not a directory.")
        sys.exit(1)

    rag_pipeline = RAGPipeline()
    rag_pipeline.ingest_documents(args.doc_dir)

    print("\nRAG Pipeline is ready. Enter your queries below. Type 'exit' or 'quit' to stop.")
    while True:
        query = input("\nEnter your query: ")
        if query.lower() in ["exit", "quit"]:
            print("Exiting RAG CLI. Goodbye!")
            break
        
        results = rag_pipeline.retrieve_information(query, k=3) # Retrieve top 3 results 
        
        if results:
            print("\n--- Retrieved Information ---")
            for i, result in enumerate(results):
                print(f"Result {i+1} (Distance: {result['distance']:.4f}):")
                print(f"  {result['metadata']['text']}\n")
        else:
            print("No relevant information found.")

if __name__ == "__main__":
    main()
