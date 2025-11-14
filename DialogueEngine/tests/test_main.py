import unittest
import httpx
from unittest.mock import patch, MagicMock
import sys
import os
import asyncio

# Temporarily add the parent directory to sys.path to allow importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ChatGPT.main import app, ADMIN_API_KEY
from ChatGPT.prompt_manager import PromptManager

class TestMainAPI(unittest.TestCase):
    def setUp(self):
        # Ensure prompt_manager is reloaded to get fresh values for each test
        from importlib import reload
        reload(sys.modules['ChatGPT.prompt_manager'])
        self.prompt_manager = PromptManager() # Use the actual prompt manager
        
        # Create an AsyncClient for testing FastAPI
        self.client = httpx.AsyncClient(app=app, base_url="http://test")

    async def async_tearDown(self):
        await self.client.aclose()

    def tearDown(self):
        # Run the async tearDown in the current event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_tearDown())

    @patch('ChatGPT.main.gpt_router')
    async def test_chat_endpoint_openai_success(self, mock_gpt_router):
        mock_gpt_router.get_gpt_response.return_value = "Mocked OpenAI chat response."
        
        response = await self.client.post(
            "/chat", 
            json={"courseId": "default", "message": "Hello", "llm_provider": "openai"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "Mocked OpenAI chat response."})
        mock_gpt_router.get_gpt_response.assert_called_once_with("default", "Hello", llm_provider="openai")

    @patch('ChatGPT.main.gpt_router')
    async def test_chat_endpoint_ollama_success(self, mock_gpt_router):
        mock_gpt_router.get_gpt_response.return_value = "Mocked Ollama chat response."
        
        response = await self.client.post(
            "/chat", 
            json={"courseId": "math101", "message": "Solve this", "llm_provider": "ollama"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "Mocked Ollama chat response."})
        mock_gpt_router.get_gpt_response.assert_called_once_with("math101", "Solve this", llm_provider="ollama")

    @patch('ChatGPT.main.gpt_router')
    async def test_chat_endpoint_error_from_gpt_router(self, mock_gpt_router):
        mock_gpt_router.get_gpt_response.return_value = "Error: Something went wrong with LLM."
        
        response = await self.client.post(
            "/chat", 
            json={"courseId": "default", "message": "Error test"}
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Error: Something went wrong with LLM."})

    async def test_update_prompt_endpoint_success(self):
        response = await self.client.post(
            "/prompts",
            headers={"X-Admin-API-Key": ADMIN_API_KEY},
            json={
                "course_id": "new_course",
                "system_message": "New system prompt",
                "user_message_template": "New user template: {user_query}"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Prompt for course 'new_course' updated successfully."})
        self.assertIsNotNone(self.prompt_manager.get_prompt("new_course"))

    async def test_update_prompt_endpoint_unauthorized(self):
        response = await self.client.post(
            "/prompts",
            headers={"X-Admin-API-Key": "wrong_key"},
            json={
                "course_id": "unauthorized_course",
                "system_message": "Unauthorized system prompt",
                "user_message_template": "Unauthorized user template: {user_query}"
            }
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Unauthorized: Invalid Admin API Key"})

    async def test_get_all_prompts_endpoint_success(self):
        response = await self.client.get(
            "/prompts",
            headers={"X-Admin-API-Key": ADMIN_API_KEY}
        )
        self.assertEqual(response.status_code, 200)
        prompts = response.json()
        self.assertIn("default", prompts)
        self.assertIn("math101", prompts)
        self.assertIn("history202", prompts)

    async def test_get_all_prompts_endpoint_unauthorized(self):
        response = await self.client.get(
            "/prompts",
            headers={"X-Admin-API-Key": "wrong_key"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Unauthorized: Invalid Admin API Key"})

    async def test_chat_ui_endpoint(self):
        response = await self.client.get("/chat_ui")
        self.assertEqual(response.status_code, 200)
        self.assertIn("GPT Course Chat", response.text)
        self.assertIn("Type your message...", response.text)
        self.assertIn('<select id="llmProvider">', response.text)
        self.assertIn('<option value="openai">OpenAI</option>', response.text)
        self.assertIn('<option value="ollama">Ollama</option>', response.text)

if __name__ == '__main__':
    # To run async tests with unittest, you need to use a test runner that supports it
    # or wrap each async test method. pytest-asyncio is a common choice.
    # For simple execution, we can manually run them in an event loop.
    # However, unittest.main() does not directly support async test methods.
    # For now, we'll just define the tests.
    # If running with pytest: pytest ChatGPT/tests/test_main.py
    unittest.main()
