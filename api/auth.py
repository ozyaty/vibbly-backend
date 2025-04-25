import os
import hmac
import hashlib
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def check_telegram_auth(init_data: str) -> dict:
    """
    Verify the initData string from Telegram and return user info dict.
    Raises HTTPException(400) if verification fails.
    """
    # 1) Parse into a dict
    params = dict(item.split("=", 1) for item in init_data.split("&"))
    
    # 2) Extract and remove the hash
    received_hash = params.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing hash")
    
    # 3) Also remove the extra "signature" field, if present
    params.pop("signature", None)

    # 4) Build the check string from the remaining keys
    data_check_arr = [f"{k}={v}" for k, v in sorted(params.items())]
    data_check_string = "\n".join(data_check_arr)

    # 5) Compute HMAC-SHA256
    computed_hash = hmac.new(SECRET_KEY, data_check_string.encode(), hashlib.sha256).hexdigest()

    # 6) Compare
    if computed_hash != received_hash:
        raise HTTPException(status_code=400, detail="Invalid hash")

    return params
