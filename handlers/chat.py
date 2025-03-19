import os
import httpx
from aiogram import Router, F, types
from aiogram.utils.markdown import hcode

router = Router()

# Инициализация клиента OpenRouter с помощью httpx
client = httpx.AsyncClient()

# Работа с OpenRouter API
@router.message(F.text)
async def chat_with_gpt(message: types.Message):
    try:
        # Отправка запроса на OpenRouter
        response = await client.post(
            'https://openrouter.ai/api/v1/chat/completions',  # API OpenRouter
            json={
                'model': 'mistralai/mistral-7b',  # Модель OpenRouter
                'messages': [
                    {"role": "system", "content": "Тебе 20 лет, ты злой и ленивый Telegram-бот-помощник."},
                    {"role": "user", "content": message.text}
                ]
            },
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"
            }
        )

        # Получаем ответ от модели и отправляем пользователю
        reply = response.json()["choices"][0]["message"]["content"]
        await message.reply(reply)

    except Exception as e:
        await message.reply(f"❌ Ошибка: {hcode(str(e))}")
