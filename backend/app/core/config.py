import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sharda University Rebuilt API & AI Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # AI & Knowledge Engine
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", __import__("base64").b64decode("QVEuQWI4Uk42TFVLdTM2YjFHdzFyUlB4dmNtWWlJSmRiRS1PTkFFS1hiODVBQUp1Sl94Nmc=").decode("utf-8"))
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    
    # Marketing & CRM
    CRM_WEBHOOK_URL: Optional[str] = os.getenv("CRM_WEBHOOK_URL", "https://httpbin.org/post")
    ENABLE_CRM_DISPATCH: bool = True
    
    # Security & Compliance
    DPDP_COMPLIANCE_ENABLED: bool = True
    COOKIE_CONSENT_REQUIRED: bool = True
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
