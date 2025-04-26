import os
import hmac
import hashlib
from urllib.parse import parse_qsl
from fastapi import HTTPException
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def verify_telegram_auth(init_data: str) -> dict:
    try:
        # 1. Parse initData
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
        received_hash = parsed_data.pop("hash", None)

        if not received_hash:
            raise HTTPException(status_code=400, detail="Missing hash")

        # 2. Build the check string
        check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))

        # 3. Compute HMAC
        computed_hash = hmac.new(
            SECRET_KEY, msg=check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()

        if computed_hash != received_hash:
            raise HTTPException(status_code=400, detail="Invalid hash")

        # 4. Parse user JSON field
        user_data = json.loads(parsed_data["user"])

        return user_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")
