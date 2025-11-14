import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_COURSE_ID: str = os.getenv("DEFAULT_COURSE_ID", "default")
    DEFAULT_GPT_MODEL: str = os.getenv("DEFAULT_GPT_MODEL", "gpt-3.5-turbo")
    
    # New configurations for Ollama integration
    OLLAMA_API_URL: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
    DEFAULT_OLLAMA_MODEL: str = os.getenv("DEFAULT_OLLAMA_MODEL", "llama2")
    
    # Option to choose between OpenAI and Ollama
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "openai").lower() # "openai" or "ollama"

    if not OPENAI_API_KEY and DEFAULT_LLM_PROVIDER == "openai":
        print("Warning: OPENAI_API_KEY not found in .env file. OpenAI API calls will fail.")
    if DEFAULT_LLM_PROVIDER == "ollama":
        print(f"Note: Using Ollama as the default LLM provider. Ensure Ollama is running at {OLLAMA_API_URL}")

config = Config()