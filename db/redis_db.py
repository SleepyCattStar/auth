import redis


from auth.config import(
    # REDIS_HOST,
    # REDIS_PORT,
    REDIS_URL
)

# redis_client = redis.Redis(
#     host = REDIS_HOST,
#     port= REDIS_PORT,
#     decode_responses=True
# )

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses = True
)