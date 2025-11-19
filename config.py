"""Загрузка настроек Telegram-бота."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Settings:
    """Контейнер с настройками приложения."""

    telegram_bot_token: str
    llm_api_key: str
    llm_model: str
    llm_api_base: str


def _get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or value.strip() == "":
        raise ValueError(f"Не задано обязательное окружение: {name}")
    return value


def get_settings() -> Settings:
    """Читает переменные окружения и возвращает объект настроек."""

    return Settings(
        telegram_bot_token=_get_env("TELEGRAM_BOT_TOKEN"),
        llm_api_key=_get_env("LLM_API_KEY"),
        llm_model=_get_env("LLM_MODEL"),
        llm_api_base=os.getenv("LLM_API_BASE", "https://api.openai.com/v1"),
    )
