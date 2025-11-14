import unittest
import numpy as np
import faiss
import sys
import os

# Add the parent directory to the sys.path to allow importing vector_db_module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from RAG.vector_db_module import VectorDB

class TestVectorDBModule(unittest.TestCase):
    def setUp(self):
        self.dimension = 128 # A common embedding dimension for testing
        self.vector_db = VectorDB(dimension=self.dimension)

    def test_initialization(self):
        self.assertIsInstance(self.vector_db.index, faiss.IndexFlatL2)
        self.assertEqual(self.vector_db.dimension, self.dimension)
        self.assertEqual(self.vector_db.index.ntotal, 0)
        self.assertEqual(len(self.vector_db.metadatas), 0)

    def test_add_vectors(self):
        embeddings = np.random.rand(10, self.dimension).astype('float32')
        metadatas = [{"id": i, "text": f"text_{i}"} for i in range(10)]
        self.vector_db.add_vectors(embeddings, metadatas)
        
        self.assertEqual(self.vector_db.index.ntotal, 10)
        self.assertEqual(len(self.vector_db.metadatas), 10)
        self.assertEqual(self.vector_db.metadatas[0]["text"], "text_0")

    def test_add_vectors_dimension_mismatch(self):
        embeddings = np.random.rand(10, self.dimension + 1).astype('float32') # Incorrect dimension
        metadatas = [{"id": i} for i in range(10)]
        with self.assertRaises(ValueError) as cm:
            self.vector_db.add_vectors(embeddings, metadatas)
        self.assertIn("Embedding dimension mismatch", str(cm.exception))

    def test_search_basic(self):
        # Add some random vectors
        embeddings = np.random.rand(10, self.dimension).astype('float32')
        metadatas = [{"id": i, "text": f"text_{i}"} for i in range(10)]
        self.vector_db.add_vectors(embeddings, metadatas)

        # Create a query embedding (e.g., one of the added embeddings)
        query_embedding = embeddings[0]
        
        results = self.vector_db.search(query_embedding, k=3)
        
        self.assertEqual(len(results), 3)
        self.assertIn("metadata", results[0])
        self.assertIn("distance", results[0])
        
        # The closest result should be the query embedding itself (distance should be very small)
        self.assertEqual(results[0]["metadata"]["id"], 0)
        self.assertLess(results[0]["distance"], 1e-6) # L2 distance of a vector to itself is 0

    def test_search_empty_db(self):
        query_embedding = np.random.rand(self.dimension).astype('float32')
        results = self.vector_db.search(query_embedding, k=1)
        self.assertEqual(len(results), 0)

    def test_search_dimension_mismatch(self):
        query_embedding = np.random.rand(self.dimension + 1).astype('float32') # Incorrect dimension
        with self.assertRaises(ValueError) as cm:
            self.vector_db.search(query_embedding, k=1)
        self.assertIn("Query embedding dimension mismatch", str(cm.exception))

    def test_search_relevance(self):
        # Create a set of embeddings where one is clearly closer to the query
        target_embedding = np.array([0.9] * self.dimension).astype('float32')
        other_embeddings = np.random.rand(9, self.dimension).astype('float32') * 0.1 # Far from target
        
        embeddings = np.vstack([target_embedding, other_embeddings])
        metadatas = [{"id": 0, "text": "Target text"}, {"id": 1, "text": "Other text 1"},
                     {"id": 2, "text": "Other text 2"}, {"id": 3, "text": "Other text 3"},
                     {"id": 4, "text": "Other text 4"}, {"id": 5, "text": "Other text 5"},
                     {"id": 6, "text": "Other text 6"}, {"id": 7, "text": "Other text 7"},
                     {"id": 8, "text": "Other text 8"}, {"id": 9, "text": "Other text 9"}]
        
        self.vector_db.add_vectors(embeddings, metadatas)

        query_embedding = np.array([0.9] * self.dimension).astype('float32') # Query is identical to target
        
        results = self.vector_db.search(query_embedding, k=1)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["metadata"]["id"], 0)
        self.assertLess(results[0]["distance"], 1e-6) # Distance should be very close to 0

if __name__ == '__main__':
    unittest.main()
