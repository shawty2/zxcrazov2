import os
import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hcode

router = Router()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Флаг включения/отключения GPT
gpt_enabled = True

@router.message(F.text == "/gpt_on")
async def enable_gpt(message: Message):
    global gpt_enabled
    gpt_enabled = True
    await message.reply("✅ GPT-чат включен.")

@router.message(F.text == "/gpt_off")
async def disable_gpt(message: Message):
    global gpt_enabled
    gpt_enabled = False
    await message.reply("❌ GPT-чат выключен.")

@router.message(F.text)
async def chat_with_gpt(message: Message):
    global gpt_enabled

    if not gpt_enabled:
        return  # GPT выключен — ничего не делаем

    user_message = message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": "Ты злой, ироничный помощник, говоришь резко, не терпишь глупых вопросов, харизматичен, умен. Отвечаешь на русском, иногда используешь популярные у молодежи смайлики, если это уместно. Также ты максимально краток."},
            {"role": "user", "content": user_message}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                await message.reply(f"❌ Ошибка {response.status_code}:\n{hcode(response.text)}")
                return

            data = response.json()

            if "choices" not in data:
                await message.reply(f"❌ В ответе нет поля 'choices':\n{hcode(str(data))}")
                return

            reply = data["choices"][0]["message"]["content"]
            await message.reply(reply)

        except Exception as e:
            await message.reply(f"❌ Ошибка при обращении к API:\n<code>{e}</code>")
