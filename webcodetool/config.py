"""Configuration management for WebCodeTool."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings.
    
    Configuration can be set via environment variables or a .env file.
    Create a .env file from .env.example to customize settings.
    """
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # Agent settings
    max_iterations: int = 10
    timeout: int = 300
    
    # Code execution settings
    enable_code_execution: bool = True
    code_execution_timeout: int = 30
    
    # API keys (optional)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
