import asyncio
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# ================== START ==================

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "<b>Напишите /help, чтобы просмотреть команды и возможности бота</b>\n\n"
        "Привет! Этот бот написан на aiogram, надеюсь вам понравится!",
        parse_mode="HTML"
    )

# ================== HELP ==================

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "<b>Вот список всех доступных команд</b>\n\n"
        "/start — начало\n"
        "/help — список команд\n"
        "/bot_photo — аватарка бота\n"
        "/bot_delete — удалить прошлое сообщение\n"
        "/bot_delete_all — удалить последние 100 сообщений",
        parse_mode="HTML"
    )

# ================== BOT PHOTO ==================

@router.message(Command("bot_photo"))
async def bot_photo(message: Message):
    photo = FSInputFile("images/github.png")
    await message.answer_photo(
        photo=photo,
        caption="<b>Bot Photo</b>",
        parse_mode="HTML"
    )

# ================== DELETE ONE ==================

@router.message(Command("bot_delete"))
async def bot_delete(message: Message):
    chat_id = message.chat.id

    try:
        await message.bot.delete_message(
            chat_id=chat_id,
            message_id=message.message_id - 1
        )
    except Exception as e:
        print(f"Delete previous message error: {e}")

    await message.delete()

# ================== DELETE MANY ==================

@router.message(Command("bot_delete_all"))
async def clear_chat(message: Message):
    chat_id = message.chat.id
    current_id = message.message_id
    limit = 100

    for msg_id in range(current_id, current_id - limit, -1):
        try:
            await message.bot.delete_message(chat_id, msg_id)
        except Exception:
            pass
# ================== MAIN ==================

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
