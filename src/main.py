from src.cfg.cfg import cfg
from src.lang.lang import lang

from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import asyncio

from commands import commands_router
from src.database.db import db_classes

WEBHOOK_URL = f'{cfg.webhook_host}{cfg.webhook_path}'  # Creating full webhook url

# We are using different bot tokens for debug and release mode.
if cfg.debug:
    bot = Bot(token=cfg.api_token_debug.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
else:
    bot = Bot(token=cfg.api_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))

dp = Dispatcher()
dp.include_router(commands_router)


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(lang.start_0)


# noinspection PyUnusedLocal,PyShadowingNames
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)


# noinspection PyUnusedLocal,PyShadowingNames
async def on_shutdown(app):
    await bot.delete_webhook()

if not cfg.debug:
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=cfg.webhook_path)
    setup_application(app, dp, bot=bot)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    if cfg.debug:
        asyncio.run(main())
    else:
        # noinspection PyUnboundLocalVariable
        web.run_app(app, host='localhost', port=3000)
