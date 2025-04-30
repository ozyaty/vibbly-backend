import os
import hmac
import hashlib
from urllib.parse import quote
from fastapi import HTTPException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set!")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def verify_telegram_auth(payload: dict) -> dict:
    try:
        received_hash = payload.pop("hash", None)
        if not received_hash:
            raise HTTPException(status_code=400, detail="Missing hash")

        # Format payload into check_string
        data_check_arr = []
        for key in sorted(payload.keys()):
            value = payload[key]
            if isinstance(value, dict):
                value = quote(str(value).replace("'", '"'), safe="")
            else:
                value = str(value)
            data_check_arr.append(f"{key}={value}")

        check_string = "\n".join(data_check_arr)

        # Generate hash
        computed_hash = hmac.new(
            SECRET_KEY,
            msg=check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if computed_hash != received_hash:
            raise HTTPException(status_code=400, detail="Invalid hash")

        # Return parsed user object
        return eval(payload["user"])

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")


def json_dumps(obj):
    import json
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
