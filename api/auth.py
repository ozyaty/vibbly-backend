import os
import hmac
import hashlib
from urllib.parse import unquote
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def check_telegram_auth(init_data: str) -> dict:
    # Decode if URL-encoded (as in Vercel frontend)
    init_data = unquote(init_data)

    params = dict(item.split("=", 1) for item in init_data.split("&"))
    received_hash = params.pop("hash", None)

    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing hash")

    data_check_arr = [f"{k}={v}" for k, v in sorted(params.items())]
    data_check_string = "\n".join(data_check_arr)

    computed_hash = hmac.new(SECRET_KEY, data_check_string.encode(), hashlib.sha256).hexdigest()

    if computed_hash != received_hash:
        raise HTTPException(status_code=400, detail="400: Invalid hash")

    return params
