from aiogram import Router, types
from aiogram.filters import Command
import asyncio

router = Router()

@router.message(Command("swaga"))
async def cmd_swaga(message: types.Message):
    await message.reply("а ты точно играешь на ластпик хускаре ???")
    await asyncio.sleep(5)
    await message.reply("сосал ?")
