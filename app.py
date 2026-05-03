from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from datetime import datetime
import json
import os

# Core imports (all modules above)
from core.router import AAROHRouter
from core.config import config
from context.short_term import ShortTermMemory

app = FastAPI(
    title="🧠 AAROH - Final Year Project API",
    description="Multimodal Context-Aware AI System | Gajula Vamshi | 221020110015",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

router = AAROHRouter()
user_contexts = {}  # In-memory context (Redis in prod)

class AAROHRequest(BaseModel):
    query: str
    user_id: str = "student_001"

class AAROHResponse(BaseModel):
    response: str
    intent_type: str
    status: str
    timestamp: str
    context_used: bool = False

@app.post("/api/v1/chat", response_model=AAROHResponse)
async def aaroh_chat(request: AAROHRequest):
    try:
        # Get user context
        context = user_contexts.get(request.user_id, {"history": []})
        
        # Route through architecture
        result = await router.route(request.query, request.user_id, context)
        
        # Process result
        if result["type"] == "chat_response":
            response_text = result["response"]
            context_used = True
        elif result["type"] == "task_result":
            response_text = result["result"].get("message", "Task completed")
            context_used = False
        else:
            response_text = result["response"]
        
        # Update context
        if "history" in context:
            context["history"].append({"user": request.query, "assistant": response_text})
            user_contexts[request.user_id] = context
        
        return AAROHResponse(
            response=response_text,
            intent_type=result.get("intent", {}).type,
            status="success",
            timestamp=datetime.now().isoformat(),
            context_used=context_used
        )
        
    except Exception as e:
         import traceback
         traceback.print_exc()   # 👈 THIS WILL PRINT REAL ERROR
         raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health():
    return {"status": "🟢 AAROH Healthy", "version": "1.0.0"}

@app.get("/api/v1/memory/{user_id}")
async def memory(user_id: str):
    mem = ShortTermMemory(user_id)
    return {"context": mem.get_context(), "length": len(mem.memory)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)