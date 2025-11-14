from flask import Flask, render_template, request, redirect, url_for
import os
import sys

# Add the parent directory to the sys.path to allow importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ContentGen.text_engine import TextEngine, get_available_ollama_models
from ContentGen.storage_core import init_db, get_all_content
from ContentGen.config import config

app = Flask(__name__)

# Initialize the database when the app starts
init_db()

# Initialize TextEngine
text_engine = TextEngine()

@app.route("/", methods=["GET"])
def index():
    """
    Renders the main page with the text generation form.
    """
    available_models = get_available_ollama_models()
    return render_template(
        "index.html", 
        prompt_text="", 
        response_text="", 
        error_message="",
        available_models=available_models,
        default_model=config.DEFAULT_OLLAMA_MODEL,
        language="English" # Default language
    )

@app.route("/generate", methods=["POST"])
def generate():
    """
    Handles text generation requests from the form.
    """
    user_prompt = request.form["prompt"]
    language = request.form["language"]
    model = request.form["model"]

    generated_text = text_engine.generate_text(user_prompt, language=language, model=model)

    available_models = get_available_ollama_models() # Re-fetch models to pass back to template
    if generated_text.startswith("Error:"):
        return render_template(
            "index.html", 
            prompt_text=user_prompt, 
            response_text="", 
            error_message=generated_text,
            available_models=available_models,
            default_model=config.DEFAULT_OLLAMA_MODEL,
            language=language, # Pass back selected language
            model=model # Pass back selected model
        )
    else:
        return render_template(
            "index.html", 
            prompt_text=user_prompt, 
            response_text=generated_text, 
            error_message="",
            available_models=available_models,
            default_model=config.DEFAULT_OLLAMA_MODEL,
            language=language, # Pass back selected language
            model=model # Pass back selected model
        )

@app.route("/history", methods=["GET"])
def history():
    """
    Displays the history of generated content.
    """
    all_content = get_all_content()
    return render_template("history.html", content_history=all_content)

if __name__ == "__main__":
    # --- IMPORTANT ---
    # For this example to work, you need to have Ollama running locally
    # and the specified models (e.g., 'llama2', 'qwen') downloaded.
    #
    # 1. Download Ollama: https://ollama.ai/download
    # 2. Run Ollama: ollama serve
    # 3. Download models: ollama run llama2, ollama run qwen
    # -----------------
    app.run(debug=True, port=5000)
