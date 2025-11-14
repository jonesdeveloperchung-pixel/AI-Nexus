import requests
import json
from typing import Dict, Any, List
import zhconv # Import zhconv
import os # Import os module
import sys # Import sys module

from ContentGen.storage_core import save_content, GeneratedContent
from ContentGen.config import config

class TextEngine:
    def __init__(self):
        self.ollama_url = config.OLLAMA_API_URL
        self.default_ollama_model = config.DEFAULT_OLLAMA_MODEL
        
        # No OpenCC initialization needed with zhconv

    def generate_text(self, prompt: str, language: str = "English", model: str = None) -> str:
        """
        Generates text using a local LLM (Ollama) and saves the content to the database.
        Converts Chinese text to Simplified or Traditional based on the 'language' parameter.
        :param prompt: The user's prompt for text generation.
        :param language: The target language/script of the generated text (e.g., "English", "Simplified Chinese", "Traditional Chinese").
        :param model: The Ollama model to use. If None, uses the default from config.
        :return: The generated text.
        """
        model_to_use = model if model else self.default_ollama_model

        payload = {
            "model": model_to_use,
            "prompt": prompt,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(self.ollama_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            
            response_data = response.json()
            generated_text = response_data.get("response", "").strip()

            # Convert Chinese text if specified
            if language == "Simplified Chinese":
                generated_text = zhconv.convert(generated_text, 'zh-cn')
            elif language == "Traditional Chinese":
                generated_text = zhconv.convert(generated_text, 'zh-tw')

            # Save the generated content to the database
            save_content(prompt=prompt, response=generated_text, language=language)

            return generated_text
        except requests.exceptions.ConnectionError:
            return f"Error: Could not connect to Ollama at {self.ollama_url}. Is Ollama running?"
        except requests.exceptions.RequestException as e:
            return f"Error during Ollama API request: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

def get_available_ollama_models() -> List[str]:
    """
    Queries the Ollama API to get a list of available models.
    """
    ollama_tags_url = config.OLLAMA_API_URL.replace("/api/generate", "/api/tags")
    try:
        response = requests.get(ollama_tags_url)
        response.raise_for_status()
        data = response.json()
        models = [m['name'] for m in data.get('models', [])]
        return models
    except requests.exceptions.ConnectionError:
        print(f"Warning: Could not connect to Ollama at {ollama_tags_url}. Is Ollama running?")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Warning: Error during Ollama API tags request: {e}")
        return []
    except Exception as e:
        print(f"Warning: An unexpected error occurred while fetching Ollama models: {e}")
        return []

if __name__ == "__main__":
    # --- IMPORTANT ---
    # For this example to work, you need to have Ollama running locally
    # and the specified model (e.g., 'llama2') downloaded.
    #
    # 1. Download Ollama: https://ollama.ai/download
    # 2. Run Ollama: ollama serve
    # 3. Download models: ollama run llama2 (or ollama run qwen)
    # -----------------

    engine = TextEngine()

    print("--- Available Ollama Models ---")
    available_models = get_available_ollama_models()
    if available_models:
        print(available_models)
    else:
        print("No Ollama models found or Ollama is not running.")

    print("--- Generating English text ---")
    english_prompt = "Write a short, creative slogan for a new coffee shop."
    english_response = engine.generate_text(english_prompt, language="English") # Use default model
    print(f"Prompt: {english_prompt}")
    print(f"Response: {english_response}\n")

    print("--- Generating Chinese text (Simplified) ---")
    chinese_simplified_prompt = "写一个关于友谊的简短句子。" # Simplified input
    # You might need to change 'qwen' to a Chinese-capable model you have downloaded
    chinese_simplified_response = engine.generate_text(chinese_simplified_prompt, language="Simplified Chinese", model="qwen2.5:0.5b") 
    print(f"Prompt: {chinese_simplified_prompt}")
    print(f"Response (Simplified): {chinese_simplified_response}\n")

    print("--- Generating Chinese text (Traditional) ---")
    chinese_traditional_prompt = "寫一個關於友誼的簡短句子。" # Traditional input
    chinese_traditional_response = engine.generate_text(chinese_traditional_prompt, language="Traditional Chinese", model="qwen2.5:0.5b") 
    print(f"Prompt: {chinese_traditional_prompt}")
    print(f"Response (Traditional): {chinese_traditional_response}\n")
