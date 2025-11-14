# AI Nexus

此專案旨在開發一個模組化、安全且可擴展的平台，整合各種 AI 功能，包括基於本地大型語言模型 (LLM) 的寫作、檢索增強生成 (RAG) 工作流程，以及基於 GPT 的對話功能。

## 目錄
1.  [功能](#功能)
2.  [設定](#設定)
    *   [先決條件](#先決條件)
    *   [複製儲存庫](#複製儲存庫)
    *   [虛擬環境與依賴項](#虛擬環境與依賴項)
    *   [.env 配置](#env-配置)
    3.  [Ollama 設定 (適用於本地 LLM)](#ollama-設定-適用於本地-llm)
4.  [使用方式](#使用方式)
    *   [知識庫平台 CLI](#知識庫平台-cli)
    *   [AI 寫作環境 Web UI](#ai-寫作環境-web-ui)
    *   [ChatGPT 整合 Web UI 與 API](#chatgpt-整合-web-ui-與-api)
5.  [測試](#測試)
6.  [未來增強功能](#未來增強功能)
7.  [貢獻](#貢獻)
8.  [許可證](#許可證)

## 功能

該平台目前包含三個主要的 MVP 組件：

*   **知識庫平台 (KnowledgeBase Platform)**：一個命令列介面，用於攝取文件、生成嵌入，並使用 FAISS 向量資料庫檢索相關資訊。
*   **AI 寫作環境 (AI Writing Environment)**：一個本地基於 Web 的介面 (Flask)，用於使用本地 LLM (Ollama) 生成文本，並將生成的內容儲存在 SQLite 資料庫中。
*   **ChatGPT 整合 (ChatGPT Integration)**：一個基於 Web 的聊天 UI (FastAPI)，允許使用者與 OpenAI 的 GPT 模型或本地 Ollama 模型互動，利用課程特定的提示。

## 設定

### 先決條件
*   **Python 3.9+**：確保您的系統已安裝 Python。
*   **Git**：用於複製儲存庫。
*   **Ollama (可選，適用於本地 LLM)**：如果您計劃將本地 LLM 用於 AI 寫作環境或 ChatGPT 整合，請從 [https://ollama.ai/download](https://ollama.ai/download) 下載並安裝 Ollama。

### 複製儲存庫
```bash
git clone <repository_url>
cd AI_Nexus # 或您複製到的位置
```

### 虛擬環境與依賴項
強烈建議使用 Python 虛擬環境。

```bash
# 從專案根目錄
python -m venv KnowledgeBase\.venv
KnowledgeBase\.venv\Scripts\Activate.ps1 # 在 Windows PowerShell 上
# 在 Linux/macOS 上：source RAG/.venv/bin/activate

pip install -r KnowledgeBase/requirements.txt
```

### .env 配置
在專案根目錄 (`D:\Workspace\ChatGPT_Website`) 中建立一個 `.env` 文件，如果您計劃使用 OpenAI 模型，請添加您的 OpenAI API 金鑰。

```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
# 可選：為 ChatGPT 整合配置預設 LLM 提供者
# DEFAULT_LLM_PROVIDER=ollama
# DEFAULT_OLLAMA_MODEL=llama2
```
將 `YOUR_API_KEY` 替換為您的實際 OpenAI API 金鑰。

### Ollama 設定 (適用於本地 LLM)
如果您安裝了 Ollama，請確保它正在運行並且您已下載必要的模型：
1.  啟動 Ollama 伺服器：`ollama serve`
2.  下載模型 (例如 Llama2, Qwen)：
    ```bash
    ollama run llama2
    ollama run qwen
    ```

## 使用方式

### 知識庫平台 CLI
知識庫平台允許您透過命令列介面攝取文件和檢索資訊。

1.  **準備文件**：建立一個目錄 (例如 `my_rag_docs`) 並將您的 `.txt` 或 `.pdf` 文件放入其中。
2.  **運行 CLI**：
    ```bash
    # 從專案根目錄
    KnowledgeBase\.venv\Scripts\python.exe KnowledgeBase/cli.py --doc_dir "path/to/your/my_rag_docs"
    ```
    將 `"path/to/your/my_rag_docs"` 替換為您的文件目錄的實際路徑。
3.  **查詢**：在提示時輸入您的查詢。輸入 `exit` 或 `quit` 停止。

### AI 寫作環境 Web UI
透過簡單的 Web 介面使用本地 LLM 生成文本。

1.  **確保 Ollama 正在運行** 並且模型已下載 (請參閱 [Ollama 設定](#ollama-設定-適用於本地-llm))。
2.  **運行 Flask 應用程式**：
    ```bash
    # 從專案根目錄
    KnowledgeBase\.venv\Scripts\python.exe ContentGen/app.py
    ```
3.  **訪問 UI**：打開您的網頁瀏覽器並前往 `http://127.0.0.1:5000`。
4.  **生成與查看歷史記錄**：輸入提示，選擇語言/模型，生成文本，並查看過去的生成記錄。

### ChatGPT 整合 Web UI 與 API
透過 Web 聊天介面或直接透過 API 端點與 GPT 或 Ollama 模型互動。

1.  **確保 `.env` 中已設定 `OPENAI_API_KEY`** (適用於 OpenAI) 或 **Ollama 正在運行** 並帶有模型 (適用於 Ollama)。
2.  **運行 FastAPI 應用程式**：
    ```bash
    # 從專案根目錄
    KnowledgeBase\.venv\Scripts\python.exe -m uvicorn DialogueEngine.main:app --reload --port 8000
    ```
3.  **訪問聊天 UI**：打開您的網頁瀏覽器並前往 `http://127.0.0.1:8000/chat_ui`。選擇您偏好的 LLM 提供者並聊天。
4.  **訪問 API 文件**：對於直接 API 互動 (例如 `/chat`, `/prompts`)，請訪問 `http://127.0.0.1:8000/docs`。

## 測試

要運行每個模組的測試：

1.  **安裝 `pytest` 和 `pytest-asyncio`**：
    ```bash
    # 從專案根目錄
    RAG\.venv\Scripts\python.exe -m pip install pytest pytest-asyncio
    ```
2.  **運行測試**：
    ```bash
    # 適用於知識庫模組測試
    KnowledgeBase\.venv\Scripts\pytest KnowledgeBase/tests/

    # 適用於 AI 寫作環境模組測試 (如果已建立)
    # KnowledgeBase\.venv\Scripts\pytest ContentGen/tests/

    # 適用於 ChatGPT 模組測試
    KnowledgeBase\.venv\Scripts\pytest DialogueEngine/tests/
    ```

## 未來增強功能
*   多管道聊天 (Telegram, 電子郵件)。
*   混合 RAG (本地 + 雲端)。
*   每個課程/學生的使用情況分析儀表板。
*   帶有回溯功能的提示版本控制。
*   檢索器和評估器的插件系統。
*   統一身份驗證與授權服務。
*   API 閘道。

## 貢獻
歡迎貢獻！請參閱 `development_and_test_plan.md` 和 `Design_Specification.md` 以獲取專案指南。

## 許可證
MIT License
Author: Jones Chung
Email: jones.developer.chung@gmail.com
