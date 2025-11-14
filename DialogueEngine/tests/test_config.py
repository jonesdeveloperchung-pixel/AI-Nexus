import unittest
import os
from unittest.mock import patch
from dotenv import load_dotenv

# Temporarily add the parent directory to sys.path to allow importing config
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import config after path modification
from ChatGPT.config import Config, config as app_config

class TestConfig(unittest.TestCase):
    def setUp(self):
        # Create a temporary .env file for testing
        self.env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')
        self.original_env_content = ""
        if os.path.exists(self.env_file_path):
            with open(self.env_file_path, 'r') as f:
                self.original_env_content = f.read()
        
        with open(self.env_file_path, 'w') as f:
            f.write("OPENAI_API_KEY=test_openai_key\n")
            f.write("DEFAULT_COURSE_ID=test_course\n")
            f.write("OLLAMA_API_URL=http://test-ollama:11434/api/generate\n")
            f.write("DEFAULT_OLLAMA_MODEL=test_llama2\n")
            f.write("DEFAULT_LLM_PROVIDER=Ollama\n")
        
        # Explicitly load dotenv after writing the temporary .env file
        load_dotenv(override=True) # Use override=True to ensure new values are loaded

        # Reload config to pick up new .env values
        from importlib import reload
        reload(sys.modules['ChatGPT.config'])
        from ChatGPT.config import config as reloaded_config
        self.config = reloaded_config

    def tearDown(self):
        # Restore original .env file
        with open(self.env_file_path, 'w') as f:
            f.write(self.original_env_content)
        
        # Reload dotenv and config to restore original values
        load_dotenv(override=True)
        from importlib import reload
        reload(sys.modules['ChatGPT.config'])

    def test_openai_api_key_loaded(self):
        self.assertEqual(self.config.OPENAI_API_KEY, "test_openai_key")

    def test_default_values_when_not_set(self):
        # Temporarily clear relevant environment variables
        original_openai_key = os.environ.pop("OPENAI_API_KEY", None)
        original_default_course_id = os.environ.pop("DEFAULT_COURSE_ID", None)
        original_ollama_api_url = os.environ.pop("OLLAMA_API_URL", None)
        original_default_ollama_model = os.environ.pop("DEFAULT_OLLAMA_MODEL", None)
        original_default_llm_provider = os.environ.pop("DEFAULT_LLM_PROVIDER", None)

        # Also ensure the .env file is empty for this test
        with open(self.env_file_path, 'w') as f:
            f.write("")
        
        # Explicitly load dotenv (should load nothing from .env)
        load_dotenv(override=True)
        
        from importlib import reload
        reload(sys.modules['ChatGPT.config'])
        from ChatGPT.config import config as default_config
        
        self.assertEqual(default_config.OPENAI_API_KEY, "")
        self.assertEqual(default_config.DEFAULT_COURSE_ID, "default")
        self.assertEqual(default_config.OLLAMA_API_URL, "http://localhost:11434/api/generate")
        self.assertEqual(default_config.DEFAULT_OLLAMA_MODEL, "llama2")
        self.assertEqual(default_config.DEFAULT_LLM_PROVIDER, "openai")
        
        # Restore original environment variables
        if original_openai_key is not None:
            os.environ["OPENAI_API_KEY"] = original_openai_key
        if original_default_course_id is not None:
            os.environ["DEFAULT_COURSE_ID"] = original_default_course_id
        if original_ollama_api_url is not None:
            os.environ["OLLAMA_API_URL"] = original_ollama_api_url
        if original_default_ollama_model is not None:
            os.environ["DEFAULT_OLLAMA_MODEL"] = original_default_ollama_model
        if original_default_llm_provider is not None:
            os.environ["DEFAULT_LLM_PROVIDER"] = original_default_llm_provider
        
        # Reload dotenv and config to pick up restored values
        load_dotenv(override=True)
        from importlib import reload
        reload(sys.modules['ChatGPT.config'])


    def test_ollama_config_loaded(self):
        self.assertEqual(self.config.OLLAMA_API_URL, "http://test-ollama:11434/api/generate")
        self.assertEqual(self.config.DEFAULT_OLLAMA_MODEL, "test_llama2")

    def test_default_llm_provider_loaded_and_lowercased(self):
        self.assertEqual(self.config.DEFAULT_LLM_PROVIDER, "ollama")

if __name__ == '__main__':
    unittest.main()