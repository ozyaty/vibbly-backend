import os
import hmac
import hashlib
from fastapi import HTTPException
from pydantic import BaseModel

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def verify_telegram_auth(data: BaseModel) -> dict:
    try:
        user_fields = {
            "auth_date": data.auth_date,
            "query_id": data.query_id,
            "user": data.user,
        }
        check_str_parts = [
            f"auth_date={user_fields['auth_date']}",
            f"query_id={user_fields['query_id']}",
            f"user={json_dumps(user_fields['user'])}",
        ]
        check_string = "\n".join(check_str_parts)

        computed_hash = hmac.new(SECRET_KEY, check_string.encode(), hashlib.sha256).hexdigest()

        if computed_hash != data.hash:
            raise HTTPException(status_code=400, detail="Invalid hash")

        return user_fields["user"]

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash validation error: {str(e)}")

def json_dumps(obj):
    import json
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
