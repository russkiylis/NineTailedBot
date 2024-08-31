from src.cfg.cfg import cfg
from src.lang.lang import lang

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import asyncio

WEBHOOK_URL = f'{cfg.webhook_host}{cfg.webhook_path}'

if cfg.debug:
    bot = Bot(token=cfg.api_token_debug.get_secret_value())
else:
    bot = Bot(token=cfg.api_token.get_secret_value())

dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(lang.start_0)


async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app):
    await bot.delete_webhook()


app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)


# Регистрация обработчиков запросов
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=cfg.webhook_path)
setup_application(app, dp, bot=bot)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    if cfg.debug:
        asyncio.run(main())
    else:
        web.run_app(app, host='localhost', port=3000)

