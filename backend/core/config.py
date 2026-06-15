import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "dummy-key")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "https://dummy.openai.azure.com/")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Terraform Review Assistant"
    UPLOAD_DIR: str = os.path.join(os.getcwd(), "uploads")
    
    class Config:
        case_sensitive = True

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
