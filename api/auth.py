import os
import hmac
import hashlib
import json
from urllib.parse import parse_qsl, unquote
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def check_telegram_auth(init_data: str) -> dict:
    """
    Correct Telegram initData validation.
    """
    try:
        # 1. Parse initData correctly
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
        received_hash = parsed_data.pop("hash", None)

        if not received_hash:
            raise HTTPException(status_code=400, detail="Missing hash")

        # 2. Sort and prepare the check string
        check_list = [f"{k}={v}" for k, v in sorted(parsed_data.items())]
        check_string = "\n".join(check_list)

        # 3. HMAC-SHA256 signature
        computed_hash = hmac.new(
            SECRET_KEY,
            msg=check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if computed_hash != received_hash:
            raise HTTPException(status_code=400, detail="Invalid hash")

        # 4. Return user data
        user_json = parsed_data.get("user")
        if user_json:
            return json.loads(user_json)

        return parsed_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")
