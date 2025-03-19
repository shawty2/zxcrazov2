import os
import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hcode

router = Router()

# Получаем API ключ из переменной окружения
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@router.message(F.text)
async def chat_with_gpt(message: Message):
    user_message = message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Подготовка payload для модели Mistral 7B Instruct Free
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",  # Используем правильный ID модели
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }

    # Используем httpx для отправки запроса к OpenRouter
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload
            )

            # Проверка статуса ответа
            if response.status_code != 200:
                await message.reply(f"❌ Ошибка {response.status_code}:\n{hcode(response.text)}")
                return

            # Получаем данные из ответа
            data = response.json()

            # Проверяем наличие поля 'choices'
            if "choices" not in data:
                await message.reply(f"❌ В ответе нет поля 'choices':\n{hcode(str(data))}")
                return

            # Извлекаем ответ модели
            reply = data["choices"][0]["message"]["content"]
            await message.reply(reply)

        except Exception as e:
            await message.reply(f"❌ Ошибка при обращении к API:\n<code>{e}</code>")
