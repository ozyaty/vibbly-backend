import os
import hmac
import hashlib
from fastapi import HTTPException

# 1) Load your Bot API token from an environment variable (set this on Railway)
BOT_TOKEN = os.getenv(8172123365:AAGb1q5Emfy4Qx06icJttwfxfFFY1kI8oEg)

# 2) Derive the secret key by taking SHA256 of the Bot token
SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def check_telegram_auth(init_data: str) -> dict:
    """
    Verify the initData string from Telegram and return user info dict.
    Raises HTTPException(400) if verification fails.
    """
    # Parse the init_data payload (URL query-string format)
    # e.g. "id=12345&first_name=Ozzy&hash=abcdef..."
    params = dict(item.split("=", 1) for item in init_data.split("&"))
    received_hash = params.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing hash")

    # Build the check string in the format key=value\nkey=value...
    data_check_arr = [f"{k}={v}" for k, v in sorted(params.items())]
    data_check_string = "\n".join(data_check_arr)

    # Compute HMAC-SHA256 of the check string using SECRET_KEY
    computed_hash = hmac.new(SECRET_KEY, data_check_string.encode(), hashlib.sha256).hexdigest()

    if computed_hash != received_hash:
        raise HTTPException(status_code=400, detail="Invalid hash")

    # If valid, return the remaining params (user info)
    return params
