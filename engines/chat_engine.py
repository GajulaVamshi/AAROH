from core.llm import AAROHTLLM
from context.short_term import ShortTermMemory
from context.semantic import SemanticMemory

class ChatEngine:
    def __init__(self):
        self.llm = AAROHTLLM()
    
    async def process(self, query: str, user_id: str, context_data: dict) -> str:
        # Multi-layer context
        short_mem = ShortTermMemory(user_id)
        sem_mem = SemanticMemory(user_id)
        
        short_context = short_mem.get_context()
        sem_context = sem_mem.retrieve_relevant(query)
        
        full_context = f"""
SHORT-TERM ({len(short_mem.memory)} exchanges):
{short_context}

SEMANTIC MEMORY (Top matches):
{sem_context}
        """
        
        response = await self.llm.generate_context_aware(
            query, full_context, context_data.get("history", [])
        )
        
        # Store interaction
        short_mem.add_exchange(query, response)
        sem_mem.store_interaction(f"User: {query}\nAAROH: {response}")
        
        return response