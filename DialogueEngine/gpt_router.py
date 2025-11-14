import openai
import requests
import json
from typing import Dict, List, Optional
from .config import config
from .prompt_manager import PromptManager

class GPTRouter:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        self.prompt_manager = PromptManager()
        self.ollama_api_url = config.OLLAMA_API_URL
        self.default_ollama_model = config.DEFAULT_OLLAMA_MODEL

    def _get_ollama_response(self, system_message: str, user_message: str, model: str) -> str:
        """
        Makes a request to the local Ollama API to get a response.
        """
        payload = {
            "model": model,
            "prompt": f"{system_message}\n\n{user_message}", # Ollama often prefers a combined prompt
            "stream": False
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(self.ollama_api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            response_data = response.json()
            return response_data.get("response", "").strip()
        except requests.exceptions.ConnectionError:
            return f"Error: Could not connect to Ollama at {self.ollama_api_url}. Is Ollama running?"
        except requests.exceptions.RequestException as e:
            return f"Error during Ollama API request: {e}"
        except Exception as e:
            return f"An unexpected error occurred with Ollama: {e}"

    def get_gpt_response(self, course_id: str, user_query: str, llm_provider: Optional[str] = None) -> str:
        """
        Retrieves an LLM response based on the course ID, user query, and specified LLM provider.
        """
        provider_to_use = (llm_provider if llm_provider else config.DEFAULT_LLM_PROVIDER).lower()

        prompt_data = self.prompt_manager.get_prompt(course_id)
        if not prompt_data:
            print(f"Warning: No specific prompt found for course ID '{course_id}'. Using default prompt.")
            prompt_data = self.prompt_manager.get_prompt("default")
            if not prompt_data:
                return "Error: No default prompt configured."

        system_message = prompt_data["system_message"]
        user_message = prompt_data["user_message_template"].format(user_query=user_query)

        if provider_to_use == "openai":
            messages: List[Dict[str, str]] = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
            try:
                chat_completion = self.openai_client.chat.completions.create(
                    model=config.DEFAULT_GPT_MODEL,
                    messages=messages
                )
                return chat_completion.choices[0].message.content
            except openai.APIError as e:
                print(f"OpenAI API Error (status_code: {e.status_code}): {e.response}") # More detailed logging
                return f"Error: An error occurred while communicating with OpenAI. Details: {e.status_code} - {e.response.json().get('error', {}).get('message', 'No message provided')}"
            except Exception as e:
                print(f"An unexpected error occurred with OpenAI: {e}")
                return f"Error: An unexpected error occurred. Details: {e}"
        elif provider_to_use == "ollama":
            return self._get_ollama_response(system_message, user_message, self.default_ollama_model)
        else:
            return f"Error: Unknown LLM provider '{provider_to_use}'."

if __name__ == "__main__":
    # Ensure you have OPENAI_API_KEY set in your .env file for OpenAI testing
    # Ensure Ollama is running locally with 'llama2' and 'qwen' models for Ollama testing
    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

    router = GPTRouter()

    print("--- Testing with default course ID ---")
    response_default_openai = router.get_gpt_response("default", "What is the capital of France?", llm_provider="openai")
    print(f"Response (default/OpenAI): {response_default_openai}\n")

    print("--- Testing with math101 course ID ---")
    # Ensure 'llama2' model is available in Ollama
    response_math_ollama = router.get_gpt_response("math101", "How do I solve for x in 2x + 5 = 11?", llm_provider="ollama")
    print(f"Response (math101/Ollama): {response_math_ollama}\n")

    print("--- Testing with history202 course ID (using default provider from config) ---")
    # This will use whatever is set in DEFAULT_LLM_PROVIDER in config.py
    response_history_config = router.get_gpt_response("history202", "Tell me about the causes of World War I.")
    print(f"Response (history202/Config Default): {response_history_config}\n")

    print("--- Testing with non-existent course ID ---")
    response_nonexistent_openai = router.get_gpt_response("nonexistent_course", "Hello there.", llm_provider="openai")
    print(f"Response (nonexistent_course/OpenAI): {response_nonexistent_openai}\n")