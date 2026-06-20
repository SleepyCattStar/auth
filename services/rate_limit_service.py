from auth.db.redis_db import redis_client
from pydantic import EmailStr

from auth.config import LOGIN_WINDOW_LIMIT,LOGIN_RATE_LIMIT



def check_login_rate_limit(ip: str, email: EmailStr):

    key = f"login_limit:{ip}:{email}"

    current = redis_client.incr(key)

    if current == 1:
        redis_client.expire(
            key,
            LOGIN_WINDOW_LIMIT
        )
    
    if current > int(LOGIN_RATE_LIMIT):
        return False
    

    return True


def get_remaining_time(email : EmailStr, ip: str):
    key = f"login_limit:{ip}:{email}"
    return redis_client.ttl(key)


# To clear the redis cache after successful authentication
def clear_login_rate_limit(
    email: EmailStr,
    ip: str
):
    key = f"login_limit:{ip}:{email}"

    redis_client.delete(key)