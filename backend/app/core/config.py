from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./jansahayak.db"
    
    # Check if we're using SQLite
    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Application
    APP_NAME: str = "JanSahayak AI"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"


settings = Settings()
