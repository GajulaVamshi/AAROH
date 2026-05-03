from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.config import config
import os

class SemanticMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        os.makedirs(config.CHROMA_PATH, exist_ok=True)
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore = Chroma(
            collection_name=f"user_{user_id}",
            persist_directory=str(config.CHROMA_PATH),
            embedding_function=self.embeddings
        )
    
    def store_interaction(self, content: str):
        splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
        texts = splitter.split_text(content)
        self.vectorstore.add_texts(
            texts=texts,
            metadatas=[{"user_id": self.user_id}] * len(texts)
        )
    
    def retrieve_relevant(self, query: str, k: int = 3) -> str:
        results = self.vectorstore.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in results])