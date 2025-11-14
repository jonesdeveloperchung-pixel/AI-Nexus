import unittest
import numpy as np
import os
import sys

# Add the parent directory to the sys.path to allow importing embedding_module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from RAG.embedding_module import get_embeddings, model # Import model to get its dimension

class TestEmbeddingModule(unittest.TestCase):
    def setUp(self):
        # Get the embedding dimension from the loaded model
        self.embedding_dimension = model.get_sentence_embedding_dimension()

    def test_get_embeddings_single_text(self):
        texts = ["This is a test sentence."]
        embeddings = get_embeddings(texts)
        
        self.assertIsInstance(embeddings, np.ndarray)
        self.assertEqual(embeddings.shape, (1, self.embedding_dimension))
        self.assertIsInstance(embeddings[0], np.ndarray)

    def test_get_embeddings_multiple_texts(self):
        texts = ["This is the first sentence.", "This is the second sentence.", "And a third one."]
        embeddings = get_embeddings(texts)
        
        self.assertIsInstance(embeddings, np.ndarray)
        self.assertEqual(embeddings.shape, (len(texts), self.embedding_dimension))
        self.assertIsInstance(embeddings[0], np.ndarray)

    def test_get_embeddings_empty_list(self):
        texts = []
        embeddings = get_embeddings(texts)
        
        self.assertIsInstance(embeddings, np.ndarray)
        self.assertEqual(embeddings.shape, (0, self.embedding_dimension)) # Expect (0, dimension) for empty input

    def test_embedding_consistency(self):
        text = "The quick brown fox jumps over the lazy dog."
        embedding1 = get_embeddings([text])
        embedding2 = get_embeddings([text])
        
        # Embeddings should be nearly identical for the same input
        np.testing.assert_allclose(embedding1, embedding2, rtol=1e-5, atol=1e-5)

if __name__ == '__main__':
    unittest.main()
