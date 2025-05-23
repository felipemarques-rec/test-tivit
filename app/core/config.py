import os
from typing import Optional


class Settings:
    """Application settings."""
    
    def __init__(self):
        self.secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
        self.algorithm: str = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/teste_tivit")
        self.external_api_base_url: str = os.getenv("EXTERNAL_API_BASE_URL", "https://api-onecloud.multicloud.tivit.com/fake")


# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

settings = Settings()
