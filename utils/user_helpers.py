from config import CACHE_FILE
import json

def load_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

user_cache = load_cache()

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(user_cache, f, ensure_ascii=False, indent=4)

async def get_user_id(message) -> int | None:
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    parts = message.text.split()
    if len(parts) > 1 and parts[1].startswith("@"):
        return user_cache.get(parts[1][1:].lower())
    return None