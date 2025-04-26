import os
import hmac
import hashlib
from urllib.parse import parse_qs, unquote_plus
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def verify_telegram_auth(init_data: str) -> dict:
    try:
        # Parse initData into dictionary
        parsed_qs = parse_qs(init_data, strict_parsing=True)

        parsed_data = {k: v[0] for k, v in parsed_qs.items()}

        received_hash = parsed_data.pop("hash", None)
        if not received_hash:
            raise HTTPException(status_code=400, detail="Missing hash")

        # Build the check string
        check_list = [f"{k}={v}" for k, v in sorted(parsed_data.items())]
        check_string = "\n".join(check_list)

        computed_hash = hmac.new(
            SECRET_KEY,
            msg=check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if computed_hash != received_hash:
            raise HTTPException(status_code=400, detail="Invalid hash")

        # If user field exists (inside initData), it's JSON encoded
        user_json = parsed_data.get("user")
        if user_json:
            import json
            return json.loads(user_json)

        return parsed_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")
