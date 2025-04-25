import os
import hmac
import hashlib
import json
from urllib.parse import parse_qsl
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def check_telegram_auth(init_data: str) -> dict:
    """
    Verify the Telegram initData string using HMAC check.
    """
    # Parse query string into dict
    parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    received_hash = parsed_data.pop("hash", None)

    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing hash")

    # Sort params and format them as key=value
    data_check_string = "\n".join(
        [f"{k}={v}" for k, v in sorted(parsed_data.items())]
    )

    # Calculate HMAC
    computed_hash = hmac.new(
        SECRET_KEY, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if computed_hash != received_hash:
        raise HTTPException(status_code=400, detail="400: Invalid hash")

    # Decode the 'user' param from JSON string into a dict
    try:
        user = json.loads(parsed_data.get("user"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user data")

    return user
