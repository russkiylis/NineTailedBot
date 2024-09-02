from src.cfg.cfg import cfg
from src.lang.lang import lang

from aiogram import Router, types
from aiogram.filters import CommandStart

commands_router = Router()


@commands_router.message(CommandStart)
async def start_handler(message: types.Message):
    await message.answer(lang.start_0)
