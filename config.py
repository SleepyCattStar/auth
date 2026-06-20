import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
MONGO_URL = os.getenv("MONGO_URL")

# useful for deploying it on aws/azure
# REDIS_PORT = os.getenv("REDIS_PORT")
# REDIS_HOST = os.getenv("REDIS_HOST")

REDIS_URL = os.getenv("REDIS_URL")

LOGIN_RATE_LIMIT = os.getenv("RATE_LIMIT")
LOGIN_WINDOW_LIMIT = os.getenv("WINDOW_SECONDS")