import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    PROJECT_NAME: str = "pragith.net"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "pragith.net"]
    
    # Theme
    THEME: str = os.getenv("THEME", "default")
    
    # Email / SMTP
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "noreply@pragith.net")
    MAIL_TO: str = os.getenv("MAIL_TO", "contact@pragith.net")
    
    # reCAPTCHA
    RECAPTCHA_SECRET_KEY: str = os.getenv("RECAPTCHA_SECRET_KEY", "")
    RECAPTCHA_SITE_KEY: str = os.getenv("RECAPTCHA_SITE_KEY", "")
    
    # Analytics
    GA_TAG: str = os.getenv("GA_TAG", "")
    HOTJAR_SITE_ID: str = os.getenv("HOTJAR_SITE_ID", "")
    CLARITY_PROJECT_ID: str = os.getenv("CLARITY_PROJECT_ID", "")

    # Dashboard Demo Access
    DASHBOARD_DEMO_URL: str = os.getenv("DASHBOARD_DEMO_URL", "https://dashboards.pragith.net")
    DASHBOARD_DEMO_USER: str = os.getenv("DASHBOARD_DEMO_USER", "")
    DASHBOARD_DEMO_PASSWORD: str = os.getenv("DASHBOARD_DEMO_PASSWORD", "")
    
    # Consulting
    HOURLY_RATE: float = float(os.getenv("HOURLY_RATE", "95.0"))
    CALENDLY_URL: str = os.getenv("CALENDLY_URL", "")
    
    # Feature Flags
    SHOW_PRODUCTS: bool = os.getenv("SHOW_PRODUCTS", "false").lower() == "true"
    
    class Config:
        case_sensitive = True

settings = Settings()
