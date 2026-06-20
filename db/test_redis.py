from auth.db.redis_db import redis_client

print(redis_client.ping())