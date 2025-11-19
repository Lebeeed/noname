"""Модуль работы с LLM."""
from __future__ import annotations

import json
import logging
from typing import Any, Dict

import httpx

from bot.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class LLMClientError(RuntimeError):
    """Базовое исключение клиента LLM."""


class LLMClient:
    """Клиент для обращения к API моделей."""

    def __init__(self, api_key: str, model: str, api_base: str) -> None:
        self.api_key = api_key
        self.model = model
        self.api_url = api_base.rstrip("/") + "/chat/completions"
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def generate_answer(self, prompt: str) -> str:
        """Отправляет запрос к модели и возвращает текст ответа."""

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error("LLM request failed: %s", exc)
            raise LLMClientError("Не удалось получить ответ модели, попробуйте повторить запрос позже.") from exc

        try:
            data = response.json()
            logger.debug("LLM raw response: %s", json.dumps(data, ensure_ascii=False))
            message = data["choices"][0]["message"]["content"].strip()
            return message
        except (KeyError, TypeError, ValueError) as exc:
            logger.error("Unexpected LLM payload: %s", exc)
            raise LLMClientError("Модель вернула неожиданный ответ, попробуйте повторить запрос позже.") from exc
