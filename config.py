import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

#Абсолютный путь к папке текущего проекта
BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

@dataclass (frozen=True)
class Settings:
    bot_token: str

def get_settings():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "Не найден BOT_TOKEN. Создайте его в .env файле"
        )
    return  Settings(bot_token=token)
