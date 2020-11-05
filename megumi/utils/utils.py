from datetime import datetime

def get_utc_timestamp() -> int:
    return int(datetime.utcnow().timestamp())