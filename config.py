
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent

environment = os.getenv("APP_ENV", "local")

env_path = BASE_DIR / f".env.{environment}"

print(env_path)
print(env_path.exists())
print(os.getenv("REDIS_URL"))

load_dotenv(env_path)

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

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URL = os.getenv("GOOGLE_REDIRECT_URL")