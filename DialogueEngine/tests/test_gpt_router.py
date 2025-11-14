import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import openai
import requests

# Temporarily add the parent directory to sys.path to allow importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ChatGPT.gpt_router import GPTRouter
from ChatGPT.config import config
from ChatGPT.prompt_manager import PromptManager

class TestGPTRouter(unittest.TestCase):
    def setUp(self):
        # Ensure config and prompt_manager are reloaded to get fresh values for each test
        from importlib import reload
        reload(sys.modules['ChatGPT.config'])
        reload(sys.modules['ChatGPT.prompt_manager'])
        
        # Patch the external dependencies at the class level or before GPTRouter is instantiated
        # For OpenAI, we'll mock the client directly
        self.mock_openai_client = MagicMock()
        # For Ollama, we'll mock the internal _get_ollama_response method
        self.patcher_ollama = patch('ChatGPT.gpt_router.GPTRouter._get_ollama_response')
        self.mock_get_ollama_response = self.patcher_ollama.start()
        self.addCleanup(self.patcher_ollama.stop)

        # Instantiate GPTRouter after mocks are set up
        self.router = GPTRouter()
        self.router.openai_client = self.mock_openai_client # Inject the mocked client
        self.router.prompt_manager = PromptManager() # Ensure fresh prompt manager

    def test_get_gpt_response_openai_success(self):
        self.mock_openai_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Mocked OpenAI response."))]
        )
        
        response = self.router.get_gpt_response("default", "Test query", llm_provider="openai")
        self.assertEqual(response, "Mocked OpenAI response.")
        self.mock_openai_client.chat.completions.create.assert_called_once()

    def test_get_gpt_response_openai_api_error(self):
        # Update the APIError mock to include the 'body' argument
        self.mock_openai_client.chat.completions.create.side_effect = openai.APIError(
            message="API Error Message", 
            request=MagicMock(), 
            body=MagicMock() # Added body argument
        )
        
        response = self.router.get_gpt_response("default", "Test query", llm_provider="openai")
        self.assertIn("An error occurred while communicating with OpenAI.", response)

    def test_get_gpt_response_ollama_success(self):
        self.mock_get_ollama_response.return_value = "Mocked Ollama response."
        
        response = self.router.get_gpt_response("default", "Test query", llm_provider="ollama")
        self.assertEqual(response, "Mocked Ollama response.")
        self.mock_get_ollama_response.assert_called_once()

    def test_get_gpt_response_ollama_connection_error(self):
        self.mock_get_ollama_response.return_value = "Error: Could not connect to Ollama at http://localhost:11434/api/generate. Is Ollama running?"
        
        response = self.router.get_gpt_response("default", "Test query", llm_provider="ollama")
        self.assertIn("Error: Could not connect to Ollama", response)

    def test_get_gpt_response_default_prompt_fallback(self):
        # Remove specific prompt to force fallback
        self.router.prompt_manager._prompts.pop("math101", None) 
        
        self.mock_openai_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Fallback response."))]
        )
        
        response = self.router.get_gpt_response("math101", "Test query", llm_provider="openai")
        self.assertEqual(response, "Fallback response.")
        # Assert that the default prompt was used
        args, kwargs = self.mock_openai_client.chat.completions.create.call_args
        self.assertIn("You are a helpful assistant.", kwargs['messages'][0]['content'])

    def test_get_gpt_response_unknown_provider(self):
        response = self.router.get_gpt_response("default", "Test query", llm_provider="unknown_provider")
        self.assertIn("Error: Unknown LLM provider 'unknown_provider'.", response)

    def test_get_gpt_response_no_default_prompt(self):
        # Clear all prompts, including default
        self.router.prompt_manager._prompts.clear()
        
        response = self.router.get_gpt_response("default", "Test query", llm_provider="openai")
        self.assertEqual(response, "Error: No default prompt configured.")

if __name__ == '__main__':
    unittest.main()