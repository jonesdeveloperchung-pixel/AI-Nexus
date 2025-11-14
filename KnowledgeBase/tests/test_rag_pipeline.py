import unittest
import os
import shutil
import sys
import numpy as np

# Add the parent directory to the sys.path to allow importing rag_pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from RAG.rag_pipeline import RAGPipeline
from RAG.embedding_module import get_embeddings # To generate query embeddings for assertions

class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_rag_temp_docs"
        os.makedirs(self.test_dir, exist_ok=True)
        self.rag_pipeline = RAGPipeline()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def _create_dummy_document(self, filename, content):
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    def test_ingest_documents(self):
        self._create_dummy_document("doc1.txt", "This is a test document about cats. Cats are furry animals.")
        self._create_dummy_document("doc2.txt", "Dogs are loyal companions. They love to play fetch.")
        
        self.rag_pipeline.ingest_documents(self.test_dir)
        
        # Assuming default chunk size of 500, each doc will produce 1 chunk
        self.assertEqual(self.rag_pipeline.vector_db.index.ntotal, 2)
        self.assertEqual(len(self.rag_pipeline.vector_db.metadatas), 2)
        self.assertIn("cats", self.rag_pipeline.vector_db.metadatas[0]["text"].lower())
        self.assertIn("dogs", self.rag_pipeline.vector_db.metadatas[1]["text"].lower())

    def test_retrieve_information_relevance(self):
        self._create_dummy_document("doc_cat.txt", "Cats are domesticated carnivorous mammals. They are often called house cats when kept as indoor pets.")
        self._create_dummy_document("doc_dog.txt", "Dogs are domesticated mammals, not typically wild animals. They are known for their loyalty and companionship.")
        
        self.rag_pipeline.ingest_documents(self.test_dir)
        
        query = "What kind of pets are loyal?"
        results = self.rag_pipeline.retrieve_information(query, k=1)
        
        self.assertEqual(len(results), 1)
        self.assertIn("dogs", results[0]["metadata"]["text"].lower())
        self.assertLess(results[0]["distance"], 20) # Expect a relatively low distance for relevant result

    def test_empty_ingestion(self):
        # Ingest from an empty directory
        self.rag_pipeline.ingest_documents(self.test_dir)
        
        self.assertEqual(self.rag_pipeline.vector_db.index.ntotal, 0)
        self.assertEqual(len(self.rag_pipeline.vector_db.metadatas), 0)

        # Ensure retrieval from empty DB doesn't crash
        query = "anything"
        results = self.rag_pipeline.retrieve_information(query, k=1)
        self.assertEqual(len(results), 0)

    def test_pipeline_end_to_end(self):
        # Create multiple documents
        self._create_dummy_document("doc_science.txt", "The Earth is the third planet from the Sun. It is the only astronomical object known to harbor life.")
        self._create_dummy_document("doc_history.txt", "World War II was a global war that lasted from 1939 to 1945. It involved the vast majority of the world's countries.")
        self._create_dummy_document("doc_space.txt", "Mars is often called the 'Red Planet' due to its reddish appearance. It is the fourth planet from the Sun.")

        # Ingest documents
        self.rag_pipeline.ingest_documents(self.test_dir)

        # Query for science
        query_science = "Tell me about planets and space."
        results_science = self.rag_pipeline.retrieve_information(query_science, k=2)
        self.assertEqual(len(results_science), 2)
        # Check if relevant documents are among the top results
        retrieved_texts_science = [r["metadata"]["text"].lower() for r in results_science]
        self.assertTrue(any("earth" in text for text in retrieved_texts_science))
        self.assertTrue(any("mars" in text for text in retrieved_texts_science))

        # Query for history
        query_history = "When was the major global conflict?"
        results_history = self.rag_pipeline.retrieve_information(query_history, k=1)
        self.assertEqual(len(results_history), 1)
        self.assertIn("world war ii", results_history[0]["metadata"]["text"].lower())


if __name__ == '__main__':
    unittest.main()
