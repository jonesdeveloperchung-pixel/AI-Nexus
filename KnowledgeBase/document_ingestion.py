import os
from typing import List
from pypdf import PdfReader, errors

def read_text_file(file_path: str) -> str:
    """
    Reads the content of a text file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def read_pdf_file(file_path: str) -> str:
    """
    Reads the content of a PDF file.
    """
    try:
        reader = PdfReader(file_path)
        text_content = ""
        for page in reader.pages:
            text_content += page.extract_text() + "\n"
        return text_content
    except errors.PdfStreamError as e:
        print(f"Error reading PDF file {file_path}: {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred while reading PDF file {file_path}: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Splits text into chunks of a specified size with optional overlap.
    """
    chunks = []
    if not text:
        return chunks

    current_position = 0
    while current_position < len(text):
        end_position = min(current_position + chunk_size, len(text))
        chunk = text[current_position:end_position]
        chunks.append(chunk)
        
        if end_position == len(text): # Reached the end of the text
            break
        
        current_position += chunk_size - overlap
        # Ensure current_position doesn't go backwards if overlap is too large
        if current_position < 0:
            current_position = 0
            
    return chunks

def load_documents_from_directory(directory_path: str) -> List[str]:
    """
    Loads all text and PDF documents from a specified directory and chunks them.
    """
    all_chunks = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            print(f"Processing file: {filename}")
            content = ""
            if filename.endswith(".txt") or filename.endswith(".md"): # Added .md
                content = read_text_file(file_path)
            elif filename.endswith(".pdf"):
                try:
                    content = read_pdf_file(file_path)
                except Exception as e:
                    print(f"Error reading PDF file {filename}: {e}")
                    continue
            
            if content:
                chunks = chunk_text(content)
                all_chunks.extend(chunks)
    return all_chunks

if __name__ == "__main__":
    # Example usage:
    # Create a dummy directory and some text files for testing
    test_dir = "test_documents"
    os.makedirs(test_dir, exist_ok=True)

    with open(os.path.join(test_dir, "doc1.txt"), "w", encoding="utf-8") as f:
        f.write("This is the first sentence of document one. " * 20 +
                "This is the second paragraph of document one. " * 15)

    with open(os.path.join(test_dir, "doc2.txt"), "w", encoding="utf-8") as f:
        f.write("Document two contains different information. " * 25)

    print(f"Loading documents from '{test_dir}'...")
    chunks = load_documents_from_directory(test_dir)

    print(f"\nTotal chunks generated: {len(chunks)}")
    if chunks:
        print("\nFirst 3 chunks:")
        for i, chunk in enumerate(chunks[:3]):
            print(f"--- Chunk {i+1} ---")
            print(chunk)
    
    # Clean up dummy directory
    import shutil
    shutil.rmtree(test_dir)
