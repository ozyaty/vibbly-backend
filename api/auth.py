import os
import hmac
import hashlib
from fastapi import HTTPException
from urllib.parse import parse_qsl, unquote_plus

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def check_telegram_auth(init_data: str) -> dict:
    # Decode and parse init_data
    init_data = unquote_plus(init_data)
    parsed = dict(parse_qsl(init_data))
    received_hash = parsed.pop("hash", None)

    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing hash")

    # Build check string
    data_check_arr = [f"{k}={v}" for k, v in sorted(parsed.items())]
    data_check_string = "\n".join(data_check_arr)

    # Calculate HMAC SHA256
    computed_hash = hmac.new(SECRET_KEY, data_check_string.encode(), hashlib.sha256).hexdigest()

    if computed_hash != received_hash:
        raise HTTPException(status_code=400, detail="400: Invalid hash")

    # Decode the nested "user" JSON
    import json
    user_data = json.loads(parsed["user"])

    return user_data
