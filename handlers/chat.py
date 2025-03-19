import os
from openai import AsyncOpenAI
from aiogram import Router, F, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.markdown import hcode

router = Router()

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"
    }
)

@router.message(F.text)
async def chat_with_gpt(message: types.Message):
    try:
        response = await client.chat.completions.create(
            model="mistralai/mistral-7b",
            messages=[
                {"role": "system", "content": "Тебе 20 лет, ты злой и ленивый Telegram-бот-помощник."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content
        await message.reply(reply)

    except Exception as e:
        await message.reply(f"❌ Ошибка: {hcode(str(e))}")
