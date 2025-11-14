import unittest
import os
import shutil
import sys
from unittest.mock import patch, mock_open

# Add the parent directory to the sys.path to allow importing document_ingestion
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from RAG.document_ingestion import read_text_file, read_pdf_file, chunk_text, load_documents_from_directory

class TestDocumentIngestion(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_temp_docs"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_read_text_file(self):
        file_path = os.path.join(self.test_dir, "test.txt")
        content = "Hello, this is a test text file."
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        read_content = read_text_file(file_path)
        self.assertEqual(read_content, content)

    def test_chunk_text_no_overlap(self):
        text = "This is a long sentence that needs to be chunked into smaller pieces for processing. Each piece will have a specific length."
        chunks = chunk_text(text, chunk_size=20, overlap=0)
        self.assertEqual(len(chunks), 7) # Corrected expected count
        self.assertEqual(chunks[0], "This is a long sente")
        self.assertEqual(chunks[1], "nce that needs to be")
        self.assertEqual(chunks[-1], "gth.") # Corrected last chunk content

    def test_chunk_text_with_overlap(self):
        text = "abcdefghijklmnopqrstuvwxyz"
        chunks = chunk_text(text, chunk_size=10, overlap=5)
        self.assertEqual(len(chunks), 5)
        self.assertEqual(chunks[0], "abcdefghij")
        self.assertEqual(chunks[1], "fghijklmno")
        self.assertEqual(chunks[2], "klmnopqrst")
        self.assertEqual(chunks[3], "pqrstuvwxy")
        self.assertEqual(chunks[4], "uvwxyz")

    def test_chunk_text_empty_input(self):
        chunks = chunk_text("", chunk_size=10)
        self.assertEqual(len(chunks), 0)

    def test_load_documents_from_directory_text(self):
        file1_path = os.path.join(self.test_dir, "doc1.txt")
        file2_path = os.path.join(self.test_dir, "doc2.txt")
        with open(file1_path, "w", encoding="utf-8") as f:
            f.write("Content of document one. " * 10)
        with open(file2_path, "w", encoding="utf-8") as f:
            f.write("Content of document two. " * 10)
        
        chunks = load_documents_from_directory(self.test_dir)
        # Assuming default chunk size of 500, each doc will produce 1 chunk
        self.assertGreater(len(chunks), 0)
        self.assertIn("Content of document one.", chunks[0])
        self.assertIn("Content of document two.", chunks[1])

    @patch('RAG.document_ingestion.PdfReader')
    def test_read_pdf_file_error_handling(self, MockPdfReader):
        # Simulate an invalid PDF file by making PdfReader raise an exception
        MockPdfReader.side_effect = Exception("Invalid PDF format")
        
        file_path = os.path.join(self.test_dir, "invalid.pdf")
        # Create a dummy file, content doesn't matter as PdfReader is mocked
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("This is not a PDF")

        content = read_pdf_file(file_path)
        self.assertEqual(content, "") # read_pdf_file should return empty string on error

        # Test load_documents_from_directory with an invalid PDF
        with patch('builtins.print') as mock_print:
            chunks = load_documents_from_directory(self.test_dir)
            # Assert that the error message was printed
            mock_print.assert_any_call(f"An unexpected error occurred while reading PDF file {file_path}: Invalid PDF format")
            pass


if __name__ == '__main__':
    unittest.main()