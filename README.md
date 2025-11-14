# AI Nexus

This project aims to develop a modular, secure, and extensible platform that integrates various AI capabilities, including local LLM-based writing, Retrieval-Augmented Generation (RAG) workflows, and GPT-based conversational features.

## Table of Contents
1.  [Features](#features)
2.  [Setup](#setup)
    *   [Prerequisites](#prerequisites)
    *   [Clone Repository](#clone-repository)
    *   [Virtual Environment & Dependencies](#virtual-environment--dependencies)
    *   [.env Configuration](#env-configuration)
    3.  [Ollama Setup (for Local LLMs)](#ollama-setup-for-local-llms)
4.  [Usage](#usage)
    *   [KnowledgeBase Platform CLI](#knowledgebase-platform-cli)
    *   [AI Writing Environment Web UI](#ai-writing-environment-web-ui)
    *   [ChatGPT Integration Web UI & API](#chatgpt-integration-web-ui--api)
5.  [Testing](#testing)
6.  [Future Enhancements](#future-enhancements)
7.  [Contributing](#contributing)
8.  [License](#license)

## Features

The platform currently includes three main MVP components:

*   **KnowledgeBase Platform**: A command-line interface for ingesting documents, generating embeddings, and retrieving relevant information using a FAISS vector database.
*   **AI Writing Environment**: A local web-based interface (Flask) for generating text using local LLMs (Ollama) and storing the generated content in an SQLite database.
*   **ChatGPT Integration**: A web-based chat UI (FastAPI) that allows users to interact with either OpenAI's GPT models or local Ollama models, leveraging course-specific prompts.

## Setup

### Prerequisites
*   **Python 3.9+**: Ensure Python is installed on your system.
*   **Git**: For cloning the repository.
*   **Ollama (Optional, for local LLMs)**: If you plan to use local LLMs for the AI Writing Environment or ChatGPT Integration, download and install Ollama from [https://ollama.ai/download](https://ollama.ai/download).

### Clone Repository
```bash
git clone <repository_url>
cd AI_Nexus # Or wherever you cloned it
```

### Virtual Environment & Dependencies
It's highly recommended to use a Python virtual environment.

```bash
# From the project root directory
python -m venv KnowledgeBase\.venv
KnowledgeBase\.venv\Scripts\Activate.ps1 # On Windows PowerShell
# On Linux/macOS: source RAG/.venv/bin/activate

pip install -r KnowledgeBase/requirements.txt
```

### .env Configuration
Create a `.env` file in the project root directory (`D:\Workspace\ChatGPT_Website`) and add your OpenAI API key if you plan to use OpenAI models.

```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
# Optional: Configure default LLM provider for ChatGPT Integration
# DEFAULT_LLM_PROVIDER=ollama
# DEFAULT_OLLAMA_MODEL=llama2
```
Replace `YOUR_OPENAI_API_KEY` with your actual OpenAI API key.

### Ollama Setup (for Local LLMs)
If you installed Ollama, ensure it's running and you have downloaded the necessary models:
1.  Start Ollama server: `ollama serve`
2.  Download models (e.g., Llama2, Qwen):
    ```bash
    ollama run llama2
    ollama run qwen
    ```

## Usage

### RAG Platform CLI
The RAG platform allows you to ingest documents and retrieve information via a command-line interface.

1.  **Prepare Documents**: Create a directory (e.g., `my_rag_docs`) and place your `.txt` or `.pdf` documents inside.
2.  **Run the CLI**:
    ```bash
    # From the project root directory
    KnowledgeBase\.venv\Scripts\python.exe KnowledgeBase/cli.py --doc_dir "path/to/your/my_rag_docs"
    ```
    Replace `"path/to/your/my_rag_docs"` with the actual path to your document directory.
3.  **Query**: Enter your queries when prompted. Type `exit` or `quit` to stop.

### AI Writing Environment Web UI
Generate text using local LLMs through a simple web interface.

1.  **Ensure Ollama is running** and models are downloaded (see [Ollama Setup](#ollama-setup-for-local-llms)).
2.  **Run the Flask application**:
    ```bash
    # From the project root directory
    KnowledgeBase\.venv\Scripts\python.exe ContentGen/app.py
    ```
3.  **Access UI**: Open your web browser and go to `http://127.0.0.1:5000`.
4.  **Generate & View History**: Enter prompts, select language/model, generate text, and view past generations.

### ChatGPT Integration Web UI & API
Interact with GPT or Ollama models via a web chat interface or directly through API endpoints.

1.  **Ensure `OPENAI_API_KEY` is set** in `.env` (for OpenAI) or **Ollama is running** with models (for Ollama).
2.  **Run the FastAPI application**:
    ```bash
    # From the project root directory
    KnowledgeBase\.venv\Scripts\python.exe -m uvicorn DialogueEngine.main:app --reload --port 8000
    ```
3.  **Access Chat UI**: Open your web browser and go to `http://127.0.0.1:8000/chat_ui`. Select your preferred LLM provider and chat.
4.  **Access API Documentation**: For direct API interaction (e.g., `/chat`, `/prompts`), visit `http://127.0.0.1:8000/docs`.

## Testing

To run the tests for each module:

1.  **Install `pytest` and `pytest-asyncio`**:
    ```bash
    # From the project root directory
    RAG\.venv\Scripts\python.exe -m pip install pytest pytest-asyncio
    ```
2.  **Run tests**:
    ```bash
    # For RAG module tests
    KnowledgeBase\.venv\Scripts\pytest KnowledgeBase/tests/

    # For AI Writing Environment module tests (if any were created)
    # KnowledgeBase\.venv\Scripts\pytest ContentGen/tests/

    # For ChatGPT module tests
    KnowledgeBase\.venv\Scripts\pytest DialogueEngine/tests/
    ```

## Future Enhancements
*   Multi-channel chat (Telegram, Email).
*   Hybrid RAG (local + cloud).
*   Analytics dashboard for usage per course/student.
*   Prompt versioning with rollback.
*   Plugin system for retrievers and evaluators.
*   Unified Authentication & Authorization Service.
*   API Gateway.

## Contributing
Contributions are welcome! Please refer to the `development_and_test_plan.md` and `Design_Specification.md` for project guidelines.

## License
MIT License
Author: Jones Chung
Email: jones.developer.chung@gmail.com
