from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    
    # Vector Database
    VECTOR_DB_NAME: str = "legal_docs"
    VECTOR_DB_MODEL: str = "all-MiniLM-L6-v2"
    VECTOR_DB_DIR: Path = Path(__file__).parent.parent / "vector_db_data"
    
    # File Handling
    SCRAPED_DIR: Path = Path(__file__).parent.parent / "scraped_pdfs"
    MAX_FILE_SIZE: int = 3145728
    ALLOWED_FILE_TYPES: list = ["application/pdf"]
    TARGET_WEBSITE: str = "https://manshurat.org/"
    MAX_PDFS_PER_CATEGORY: int = 3

    
    # External Tools
    TESSERACT_CMD: str  
    
    class Config:
        env_file = ".env"

    def __init__(self, **data):
        super().__init__(**data)
        self.VECTOR_DB_DIR.mkdir(exist_ok=True)
        self.SCRAPED_DIR.mkdir(exist_ok=True)

    @property
    def vector_db_config(self) -> dict:
        return {
            "name": self.VECTOR_DB_NAME,
            "embedding_model": self.VECTOR_DB_MODEL,
            "path": str(self.VECTOR_DB_DIR)
        }

settings = Settings()