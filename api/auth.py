import hmac
import hashlib
from urllib.parse import parse_qsl

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
BOT_TOKEN_BYTES = BOT_TOKEN.encode()

def check_telegram_auth(init_data: str) -> dict:
    parsed_data = dict(parse_qsl(init_data, keep_blank_values=True))
    if "hash" not in parsed_data:
        raise ValueError("No hash in init data")

    auth_hash = parsed_data.pop("hash")
    data_check_string = "\n".join(
        sorted(f"{k}={v}" for k, v in parsed_data.items())
    )
    secret_key = hashlib.sha256(BOT_TOKEN_BYTES).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, auth_hash):
        raise ValueError("Invalid hash")

    return parsed_data