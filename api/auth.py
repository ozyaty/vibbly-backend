import os
import hmac
import hashlib
import json
from urllib.parse import urlencode
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def verify_telegram_auth(data: dict) -> dict:
    """
    Correct Telegram initData validation from dict.
    """
    try:
        # 1. Prepare the check string correctly
        check_list = []
        for key in sorted(data.keys()):
            if key != "hash":
                value = data[key]
                if isinstance(value, dict):
                    value = json.dumps(value, separators=(",", ":"), ensure_ascii=False)
                else:
                    value = str(value)
                check_list.append(f"{key}={value}")
        check_string = "\n".join(check_list)

        received_hash = data.get("hash")
        if not received_hash:
            raise HTTPException(status_code=400, detail="Missing hash")

        # 2. HMAC-SHA256 signature
        computed_hash = hmac.new(
            SECRET_KEY,
            msg=check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if computed_hash != received_hash:
            raise HTTPException(status_code=400, detail="Invalid hash")

        # 3. Return user object
        return data.get("user", {})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")
