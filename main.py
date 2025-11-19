"""Точка входа Telegram-бота проректора."""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.handlers import get_router
from bot.llm_client import LLMClient
from config import get_settings


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    settings = get_settings()
    bot = Bot(token=settings.telegram_bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher()

    llm_client = LLMClient(
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        api_base=settings.llm_api_base,
    )

    dispatcher.include_router(get_router(llm_client))

    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Bot started. Waiting for updates...")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
