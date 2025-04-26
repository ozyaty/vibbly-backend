import os
import hmac
import hashlib
import json
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def verify_telegram_auth(data: dict) -> dict:
    """
    Validate Telegram initData (already parsed dict).
    """
    try:
        received_hash = data.pop("hash", None)
        if not received_hash:
            raise HTTPException(status_code=400, detail="Missing hash")

        # Rebuild check_string properly
        check_list = []
        for key in sorted(data.keys()):
            value = data[key]
            if isinstance(value, dict):
                # 👇 This is the crucial fix:
                value = json.dumps(value, separators=(",", ":"), ensure_ascii=False)
            else:
                value = str(value)
            check_list.append(f"{key}={value}")

        check_string = "\n".join(check_list)

        computed_hash = hmac.new(
            SECRET_KEY,
            msg=check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if computed_hash != received_hash:
            raise HTTPException(status_code=400, detail="Invalid hash")

        return data.get("user", {})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")
