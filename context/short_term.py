from collections import deque
from datetime import datetime
from typing import List, Dict
from core.config import config

class ShortTermMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory = deque(maxlen=config.MAX_MEMORY)
    
    def add_exchange(self, user_query: str, ai_response: str):
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_query,
            "assistant": ai_response
        })
    
    def get_context(self) -> str:
        context_parts = []
        for exchange in list(self.memory)[-4:]:
            context_parts.append(f"User: {exchange['user']}")
            context_parts.append(f"AAROH: {exchange['assistant']}")
        return "\n".join(context_parts)