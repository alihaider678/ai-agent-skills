import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 1. Paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / "db" / "chroma_store" # Where the brain lives
    
    # 2. Database Settings
    COLLECTION_NAME = "ai_tutor_knowledge" # The 'Table' name in our DB
    
    # 3. Model Settings
    # We use this specific model because it is cheap and very accurate
    EMBEDDING_MODEL = "text-embedding-3-small" 
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = Config()