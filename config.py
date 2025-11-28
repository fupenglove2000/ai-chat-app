import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

    # System prompts for different modes
    SYSTEM_PROMPTS = {
        "assistant": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses.",
        "coder": "You are an expert programmer. Help users write, debug, and explain code. Use code blocks with proper syntax highlighting.",
        "writer": "You are a creative writing assistant. Help users with writing tasks including stories, articles, emails, and more.",
        "translator": "You are a professional translator. Help users translate text between languages accurately while preserving meaning and tone.",
    }


config = Config()
