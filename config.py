from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Config:

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    EMAIL_USER = os.getenv("EMAIL_USER")

    EMAIL_PASS = os.getenv("EMAIL_PASS")

    EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    CACHE_DIAS = int(os.getenv("CACHE_DIAS",180))

    LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")
