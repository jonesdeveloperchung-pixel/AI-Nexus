import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    OLLAMA_API_URL: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
    DEFAULT_OLLAMA_MODEL: str = os.getenv("DEFAULT_OLLAMA_MODEL", "llama2")

    print(f"Note: Using Ollama API at {OLLAMA_API_URL} with default model {DEFAULT_OLLAMA_MODEL}")

config = Config()
