from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.reply(
        "/ban @user или реплай — забанить\n"
        "/kick @user или реплай — кикнуть\n"
        "/mute @user или реплай — замутить\n"
        "/unmute @user или реплай — размутить\n"
        "/chat — общение с гпт"
        "/help — твоя мать шалава"
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Сао. Что с еблом ? 💀💀💀" «\n» "Пиши /swaga , если не очкун" «\n» "Пиши /help , если беспомощный") 
