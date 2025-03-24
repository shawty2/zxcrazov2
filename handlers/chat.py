import os
import json
import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hcode

router = Router()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SESSIONS_FILE = "sessions.json"

# Флаг включения/отключения GPT
gpt_enabled = True

# Хранилище сессий пользователей
if os.path.exists(SESSIONS_FILE):
    with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
        sessions = json.load(f)
else:
    sessions = {}

DEFAULT_PROMPT = "Ты злой, ироничный помощник, говоришь резко, не терпишь глупых вопросов, харизматичен, умен. Отвечаешь на русском. Также ты краток."
ADMIN_ID = "1775773652"

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

@router.message(F.text == "/reset")
async def reset_memory(message: Message):
    user_id = str(message.from_user.id)
    if user_id in sessions:
        del sessions[user_id]
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
        await message.reply("🧠 Память очищена.")
    else:
        await message.reply("ℹ️ У тебя пока нет сохранённой истории.")

@router.message(F.text == "/memory")
async def memory_info(message: Message):
    user_id = str(message.from_user.id)
    count = len(sessions.get(user_id, {}).get("history", []))
    await message.reply(f"🧠 В твоей памяти сохранено {count} сообщений.")

@router.message(F.text == "/prompt")
async def show_prompt(message: Message):
    user_id = str(message.from_user.id)
    prompt = sessions.get(user_id, {}).get("prompt", DEFAULT_PROMPT)
    await message.reply(f"📜 Текущий системный промт: {prompt}")

@router.message(F.text.startswith("/setprompt "))
async def set_prompt(message: Message):
    user_id = str(message.from_user.id)
    new_prompt = message.text[len("/setprompt "):].strip()
    if not new_prompt:
        await message.reply("⚠️ Не удалось обновить промт. Сообщение было пустым.")
        return

    if user_id not in sessions:
        sessions[user_id] = {}
    sessions[user_id]["prompt"] = new_prompt
    sessions[user_id]["history"] = []

    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)

    await message.reply("✅ Новый системный промт сохранён и память сброшена.")

@router.message(F.text == "/allprompts")
async def all_prompts(message: Message):
    if str(message.from_user.id) != ADMIN_ID:
        await message.reply("🚫 Команда доступна только администратору.")
        return

    text = "📋 Все кастомные промты пользователей:"
    for user_id, data in sessions.items():
        prompt = data.get("prompt")
        if prompt and prompt != DEFAULT_PROMPT:
            text += f"👤 {user_id}:{prompt}"
    if text.strip() == "📋 Все кастомные промты пользователей:":
        text += "Пользователи с кастомными промтами не найдены."
    await message.reply(text)

@router.message(F.text)
async def chat_with_gpt(message: Message):
    global gpt_enabled

    if not gpt_enabled:
        return

    user_id = str(message.from_user.id)
    user_message = message.text

    if user_id not in sessions:
        sessions[user_id] = {"prompt": DEFAULT_PROMPT, "history": []}

    if not sessions[user_id].get("history"):
        sessions[user_id]["history"] = [{"role": "system", "content": sessions[user_id]["prompt"]}]

    sessions[user_id]["history"].append({"role": "user", "content": user_message})

    if len(sessions[user_id]["history"]) > 100:
        sessions[user_id]["history"] = sessions[user_id]["history"][-100:]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": sessions[user_id]["history"]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                await message.reply(f"❌ Ошибка {response.status_code}:{hcode(response.text)}")
                return

            data = response.json()

            if "choices" not in data:
                await message.reply(f"❌ В ответе нет поля 'choices':{hcode(str(data))}")
                return

            reply = data["choices"][0]["message"]["content"]
            sessions[user_id]["history"].append({"role": "assistant", "content": reply})

            with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(sessions, f, ensure_ascii=False, indent=2)

            await message.reply(reply)

        except Exception as e:
            await message.reply(f"❌ Ошибка при обращении к API:<code>{e}</code>")