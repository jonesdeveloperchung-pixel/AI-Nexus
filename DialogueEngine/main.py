from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict

from .config import config
from .gpt_router import GPTRouter
from .prompt_manager import PromptManager

app = FastAPI()
gpt_router = GPTRouter()
prompt_manager = PromptManager() # Re-initialize to ensure default prompts are loaded

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="DialogueEngine/templates")

# --- Authentication (Basic MVP) ---
# In a real application, this would involve proper user management, JWTs, etc.
# For MVP, we'll use a simple API key in the header for "admin" access.
ADMIN_API_KEY = "supersecretadminkey" # This should ideally come from environment variables

async def verify_admin_key(x_admin_api_key: str = Header(...)):
    if x_admin_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Admin API Key")
    return True

# --- Request Models ---
class ChatRequest(BaseModel):
    courseId: str
    message: str
    llm_provider: Optional[str] = None # New field for LLM provider

class PromptUpdateRequest(BaseModel):
    course_id: str
    system_message: str
    user_message_template: str

# --- API Endpoints ---

@app.get("/")
async def read_root():
    return RedirectResponse(url="/chat_ui")

@app.get("/chat_ui", response_class=HTMLResponse)
async def chat_ui(request: Request):
    """
    Renders the chat UI page.
    """
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint for student chat interactions.
    Routes the message to the appropriate GPT model based on courseId and llm_provider.
    """
    response_content = gpt_router.get_gpt_response(
        request.courseId, 
        request.message, 
        llm_provider=request.llm_provider
    )
    if "error" in response_content.lower(): # Simple check for error messages from GPTRouter
        raise HTTPException(status_code=500, detail=response_content)
    return {"response": response_content}

@app.post("/prompts", dependencies=[Depends(verify_admin_key)])
async def update_prompt_endpoint(request: PromptUpdateRequest):
    """
    Admin-only endpoint to add or update prompts for specific course IDs.
    Requires X-Admin-API-Key in header.
    """
    prompt_manager.add_prompt(
        course_id=request.course_id,
        system_message=request.system_message,
        user_message_template=request.user_message_template
    )
    return {"message": f"Prompt for course '{request.course_id}' updated successfully."}

@app.get("/prompts")
async def get_all_prompts_endpoint(admin_verified: bool = Depends(verify_admin_key)):
    """
    Admin-only endpoint to retrieve all stored prompts.
    Requires X-Admin-API-Key in header.
    """
    return prompt_manager.get_all_prompts()

# --- How to run this FastAPI application ---
# 1. Make sure you have uvicorn installed: pip install uvicorn
# 2. Run from your terminal in the project root:
#    RAG\.venv\Scripts\python.exe -m uvicorn ChatGPT.main:app --reload --port 8000
# 3. Access the API at http://127.0.0.1:8000
# 4. Access the interactive API documentation (Swagger UI) at http://127.0.0.1:8000/docs
