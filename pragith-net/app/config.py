import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)
    PROJECT_NAME: str = "pragith.net"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "pragith.net"]
    
    # Theme
    THEME: str = os.getenv("THEME", "default")

    # Navigation Layout
    NAV_MODE: str = os.getenv("NAV_MODE", "top").lower()  # top | left
    NAV_OFFSET_TOP: str = os.getenv("NAV_OFFSET_TOP", "0px")
    NAV_OFFSET_LEFT: str = os.getenv("NAV_OFFSET_LEFT", "0px")
    NAV_LEFT_WIDTH: str = os.getenv("NAV_LEFT_WIDTH", "280px")
    
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
    
    # Feature Flags
    SHOW_PRODUCTS: bool = os.getenv("SHOW_PRODUCTS", "false").lower() == "true"
    
settings = Settings()
