from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from core.config import config
import asyncio

class AAROHTLLM:
    def __init__(self):
        self.model = ChatGroq(
            groq_api_key=config.GROQ_API_KEY,
            model_name="llama3-70b-8192",  # High-quality reasoning
            temperature=0.1,
            max_tokens=2048
        ) if config.GROQ_API_KEY else None
    
    async def generate_context_aware(self, query: str, context: str, history: list) -> str:
        if not self.model:
            return "❌ LLM unavailable. Check API key."
        
        # Structured prompt with context injection
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are AAROH, a multimodal context-aware AI assistant.
Key capabilities:
- Understand conversation context
- Execute structured tasks safely
- Provide helpful, concise responses
- Reference provided context when relevant

CONTEXT: {context}"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{query}")
        ])
        
        messages = []
        for msg in history[-6:]:  # Last 6 exchanges
            messages.append(HumanMessage(content=msg['user']))
            messages.append(AIMessage(content=msg['assistant']))
        
        chain = prompt_template | self.model
        response = await chain.ainvoke({
            "context": context,
            "query": query,
            "history": messages
        })
        
        return response.content