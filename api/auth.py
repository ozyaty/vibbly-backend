import os
import hmac
import hashlib
from urllib.parse import unquote
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def check_telegram_auth(init_data: str) -> dict:
    try:
        init_data = unquote(init_data)
        pairs = [s.split("=", 1) for s in init_data.split("&")]
        data = {}

        for key, value in pairs:
            data[key] = value

        hash_value = data.pop('hash', None)
        if not hash_value:
            raise HTTPException(status_code=400, detail="Missing hash")

        check_list = [f"{k}={v}" for k, v in sorted(data.items())]
        check_string = "\n".join(check_list)

        computed_hash = hmac.new(SECRET_KEY, check_string.encode(), hashlib.sha256).hexdigest()

        if computed_hash != hash_value:
            raise HTTPException(status_code=400, detail="Invalid hash")

        return data

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")
