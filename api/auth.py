import os
import hmac
import hashlib
from urllib.parse import unquote
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def verify_telegram_auth(init_data: str) -> dict:
    try:
        # Only decode once
        init_data = unquote(init_data)
        params = dict(pair.split("=", 1) for pair in init_data.split("&"))
        
        received_hash = params.pop("hash", None)
        if not received_hash:
            raise HTTPException(status_code=400, detail="Missing hash")

        check_string = "\n".join(
            [f"{k}={v}" for k, v in sorted(params.items())]
        )

        computed_hash = hmac.new(
            SECRET_KEY,
            msg=check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if computed_hash != received_hash:
            raise HTTPException(status_code=400, detail="Invalid hash")

        # After verifying, return the full parsed params
        return params

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")
