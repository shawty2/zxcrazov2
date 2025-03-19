import os
import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hcode

router = Router()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@router.message(F.text)
async def chat_with_gpt(message: Message):
    user_message = message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "YourAppName"
    }

    payload = {
        "model": "mistralai/mistral-7b",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

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
