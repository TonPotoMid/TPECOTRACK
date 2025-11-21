from datetime import timedelta

SECRET_KEY = "change-me-to-a-secure-random-string"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def get_access_token_expire() -> int:
    return ACCESS_TOKEN_EXPIRE_MINUTES
