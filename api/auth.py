import os
import hmac
import hashlib
from urllib.parse import unquote
from fastapi import HTTPException

# ✅ Load your bot token from environment (make sure it's set in Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment!")

# ✅ Derive secret key
SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def check_telegram_auth(init_data: str) -> dict:
    """
    Validates Telegram Web App initData using HMAC-SHA256.
    """
    try:
        init_data = unquote(init_data)  # Important: URL-decode it
        pairs = [s.split("=", 1) for s in init_data.split("&")]
        data_dict = dict(pairs)

        received_hash = data_dict.pop("hash", None)
        if not received_hash:
            raise HTTPException(status_code=400, detail="Missing hash")

        # Build check_string in key=value\nkey=value... format
        check_arr = [f"{k}={v}" for k, v in sorted(data_dict.items())]
        check_string = "\n".join(check_arr)

        computed_hash = hmac.new(
            SECRET_KEY, msg=check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()

        if computed_hash != received_hash:
            raise HTTPException(status_code=400, detail="Invalid hash")

        return data_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")
