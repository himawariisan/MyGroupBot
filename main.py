import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from keyboards import (
    DAYS,
    build_days_keyboard,
    build_pairs_keyboard,
    get_user_matrix,
    users_db    
)

from database import init_db
from commands import BOT_COMMANDS

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

from aiogram.client.session.aiohttp import AiohttpSession
session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=BOT_TOKEN, session=session)


dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.answer(f"Hi, {message.from_user.first_name}! Use /my_schedule to set up your classes.")


@dp.message(Command(commands=["my_schedule"]))
async def my_schedule_command(message: types.Message):
    get_user_matrix(message.from_user.id)
    users_db[message.from_user.id]["name"] = message.from_user.first_name

    await message.answer("Select a day:", reply_markup=build_days_keyboard())


@dp.callback_query(F.data.startswith("day_"))
async def process_day_selection(callback: types.CallbackQuery):
    d_idx = int(callback.data.split("_")[1])
    day_name = DAYS[d_idx]

    await callback.message.edit_text(
        f"Selected day: {day_name}\nSelect a pair:", 
        reply_markup=build_pairs_keyboard(callback.from_user.id, d_idx),
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("toggle_"))
async def process_pair_toggle(callback: types.CallbackQuery):
    _, d_idx, p_idx = callback.data.split("_")
    d_idx, p_idx = int(d_idx), int(p_idx)

    matrix = get_user_matrix(callback.from_user.id)
    matrix[d_idx, p_idx] = 0 if matrix[d_idx][p_idx] == 1 else 1

    await callback.message.edit_reply_markup(
        reply_markup=build_pairs_keyboard(callback.from_user.id, d_idx)
    )
    await callback.answer()


@dp.callback_query(F.data == "back_to_days")
async def process_back_to_days(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Select a day:", 
        reply_markup=build_days_keyboard()
    )
    await callback.answer()


async def main():
    init_db()
    await bot.set_my_commands(BOT_COMMANDS)

    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


