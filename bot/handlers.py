"""Обработчики Telegram-бота."""
from __future__ import annotations

import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from aiogram.enums import ChatAction

from bot.llm_client import LLMClient, LLMClientError
from bot.prompts import build_user_prompt

logger = logging.getLogger(__name__)

HELP_EXAMPLES = (
    "• Какие основные направления молодежной политики в вузе?\n"
    "• Как объяснить студентам, что такое молодежный проект?\n"
    "• Сформулируй короткий анонс мероприятия по студенческому самоуправлению."
)


def get_router(llm_client: LLMClient) -> Router:
    """Создает роутер с обработчиками и внедряет клиент LLM."""

    router = Router(name="youth_policy_bot")

    @router.message(CommandStart())
    async def handle_start(message: Message) -> None:
        text = (
            "Здравствуйте! Я ИИ-помощник проректора по молодежной политике.\n"
            "Могу: \n"
            "1. Подсказать направления и инструменты молодежной политики ИГУ.\n"
            "2. Помочь с формулировками писем, анонсов и ответов студентам.\n"
            "3. Быстро структурировать справки и тезисы по запросу."
        )
        await message.answer(text)

    @router.message(Command("help"))
    async def handle_help(message: Message) -> None:
        text = (
            "Задайте вопрос в свободной форме. Например:\n"
            f"{HELP_EXAMPLES}\n\n"
            "Я отвечаю кратко (3–7 пунктов), по существу и на русском языке."
        )
        await message.answer(text)

    @router.message()
    async def handle_message(message: Message) -> None:
        user_text = (message.text or "").strip()
        if not user_text:
            await message.answer("Пожалуйста, отправьте текстовый запрос.")
            return

        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        prompt = build_user_prompt(user_text)

        try:
            answer = await llm_client.generate_answer(prompt)
        except LLMClientError:
            logger.exception("LLM error while processing message")
            await message.answer(
                "Извините, сейчас возникла техническая неполадка при обращении к языковой модели. Попробуйте повторить запрос чуть позже."
            )
            return

        await message.answer(answer)

    return router
