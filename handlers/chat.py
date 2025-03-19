import os
from openrouter import Client  # Используем OpenRouter
from aiogram import Router, F, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.markdown import hcode

router = Router()

# Инициализация клиента OpenRouter
client = Client(api_key=os.getenv("OPENROUTER_API_KEY"))

@router.message(F.text)
async def chat_with_gpt(message: types.Message):
    try:
        # Отправка запроса на OpenRouter
        response = await client.chat_completions.create(
            model="mistralai/mistral-7b",  # Модель OpenRouter
            messages=[
                {"role": "system", "content": "Ты хороший помощник!"},
                {"role": "user", "content": message.text}
            ]
        )

        # Получаем ответ от модели и отправляем пользователю
        reply = response["choices"][0]["message"]["content"]
        await message.reply(reply)

    except Exception as e:
        await message.reply(f"❌ Ошибка: {hcode(str(e))}")
