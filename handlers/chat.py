from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.chat import ChatState
import openai
import os
from config import OPENAI_API_KEY

router = Router()

# Настройка OpenRouter
openai.api_key = OPENAI_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"
openai.default_headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

user_sessions = {}

@router.message(Command("chat"))
async def start_chat(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_sessions[user_id] = [
        { "role": "system", "content": "Ты дружелюбный помощник." }
    ]
    await state.set_state(ChatState.chatting)
    await message.answer("💬 Ты начал чат со мной. Пиши, что хочешь!")

@router.message(ChatState.chatting)
async def handle_chat(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    prompt = message.text

    if user_id not in user_sessions:
        user_sessions[user_id] = [
            { "role": "system", "content": "Ты дружелюбный помощник." }
        ]

    user_sessions[user_id].append({ "role": "user", "content": prompt })

    try:
        response = await ask_chatgpt(user_sessions[user_id])
        user_sessions[user_id].append({ "role": "assistant", "content": response })
        await message.answer(response)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
        await state.clear()
        user_sessions.pop(user_id, None)

async def ask_chatgpt(messages: list[dict]) -> str:
    completion = await openai.ChatCompletion.acreate(
        model="openai/gpt-3.5-turbo",  # Укажи здесь актуальную модель, доступную в твоем OpenRouter аккаунте
        messages=messages
    )
    return completion.choices[0].message.content
