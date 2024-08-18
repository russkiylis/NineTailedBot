from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

API_TOKEN = '7299058586:AAHNcHYb4T-i7VAb0RHVJ6EqfxtEC1PjGMk'
WEBHOOK_HOST = 'https://koshy.ru'
WEBHOOK_PATH = '/webhook/ninetailedbot'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! Это бот на вебхуках.")


async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app):
    await bot.delete_webhook()


app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)


# Регистрация обработчиков запросов
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)


if __name__ == '__main__':
    asyncio.run(ma)
    web.run_app(app, host='localhost', port=3000)
