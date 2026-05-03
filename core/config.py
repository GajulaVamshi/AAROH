import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class AAROHConfig:
    # LLM
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Paths
    DATA_PATH = Path("./data")
    CHROMA_PATH = DATA_PATH / "chroma"
    USER_PROFILES = DATA_PATH / "user_profiles"
    
    # System
    MAX_MEMORY = 15
    SAFETY_ENABLED = True
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Email
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

config = AAROHConfig()
config.DATA_PATH.mkdir(exist_ok=True)
config.CHROMA_PATH.mkdir(exist_ok=True)
config.USER_PROFILES.mkdir(exist_ok=True)