from aiogram import Router, types
from aiogram.filters import Command
from utils.user_helpers import get_user_id

router = Router()

@router.message(Command("ban"))
async def cmd_ban(message: types.Message):
    user_id = await get_user_id(message)
    if not user_id:
        return await message.reply("❌ Не удалось найти пользователя.")
    try:
        await message.bot.ban_chat_member(message.chat.id, user_id)
        await message.reply("✅ Пользователь забанен.")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка при бане: {e}")

@router.message(Command("kick"))
async def cmd_kick(message: types.Message):
    user_id = await get_user_id(message)
    if not user_id:
        return await message.reply("❌ Не удалось найти пользователя.")
    try:
        await message.bot.ban_chat_member(message.chat.id, user_id)
        await message.bot.unban_chat_member(message.chat.id, user_id)
        await message.reply("👢 Пользователь кикнут.")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка при кике: {e}")

@router.message(Command("mute"))
async def cmd_mute(message: types.Message):
    user_id = await get_user_id(message)
    if not user_id:
        return await message.reply("❌ Не удалось найти пользователя.")
    try:
        await message.bot.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=types.ChatPermissions(can_send_messages=False)
        )
        await message.reply("🔇 Пользователь замучен.")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка при муте: {e}")

@router.message(Command("unmute"))
async def cmd_unmute(message: types.Message):
    user_id = await get_user_id(message)
    if not user_id:
        return await message.reply("❌ Не удалось найти пользователя.")
    try:
        await message.bot.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=types.ChatPermissions(can_send_messages=True)
        )
        await message.reply("🔊 Пользователь размучен.")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка при размуте: {e}")