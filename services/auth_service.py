from datetime import timedelta,datetime
from jose import jwt,JWTError
from passlib.context import CryptContext
from auth.config import SECRET_KEY as secret,ALGORITHM as algo ,ACCESS_TOKEN_EXPIRE_MINUTES as accesstokenminutes

from auth.schemas.user import User,UserInDB,UserCreate
from auth.schemas.token import Token,TokenData
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from auth.db.mongodb import user_collection
from auth.db.mongodb import refresh_tokens_collection

import uuid # for refresh tokens

SECRET_KEY= secret 
ALGORITHM = algo  or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(accesstokenminutes or 30)

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):

    to_encode = data.copy()

    expiry = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update(
        {"exp" : expiry}
    )

    jwt_token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm= ALGORITHM
    )

    return jwt_token


def decode_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None
    

# preventing duplicate username, email registrations
def get_user_by_email(email: str):

    user = user_collection.find_one(
        {"email":email}
    )
    
    return user

def get_user_by_username(username : str):

    duplicate_user = user_collection.find_one({
        "username" :username
    })

    return duplicate_user

def authenticate_user(email: str, password: str):
    user= get_user_by_email(email)

    if not user: 
        return None
    
    if user["locked_until"]:
        if datetime.now() < user["locked_until"]:
            raise HTTPException(
                status_code=423,
                detail="Account temporarily locked"
            )

    stored_hash = user["hashed_password"]

    if not verify_password(
        password,
        stored_hash
    ):
        failed_attempts = user["failed_attempts"] + 1

        update_data = {
            "failed_attempts": failed_attempts
        }

        if failed_attempts >= 5:
            update_data["locked_until"] = (
                datetime.now() + timedelta(minutes=15)
            )

        user_collection.update_one(
            {"email": email},
            {"$set": update_data}
        )

        return None

    # if the authentication is successful
    user_collection.update_one(
    {"email": email},
    {
        "$set": {
            "failed_attempts": 0,
            "locked_until": None
        }
    }
    )
    return user

#Registration

def register_user(user: UserCreate):

    existing_user = get_user_by_email(user.email)

    if  existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = get_user_by_username(user.username)

    if existing_username:
        raise HTTPException(status_code=400,detail="Username Already Registered")

    passwd_hashed = get_password_hash(user.password)

    user_data = {
        "username": user.username,
        "email" : user.email,
        "full_name" : user.full_name,
        "provider": "local",
        "google_id": None,
        "disabled" :user.disabled,
        "hashed_password": passwd_hashed,
        "failed_attempts": 0,
        "locked_until": None
    }

    user_collection.insert_one(user_data)

    return User(
    username=user.username,
    email=user.email,
    full_name=user.full_name,
    disabled=user.disabled
)


def get_current_user(token : str):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401,detail="Invalid Token")

    email = payload.get("sub")

    if not email:
        return None
    
    user = get_user_by_email(email=email)

    return user
    

# WRITE THIS FUNCTION

def create_refresh_token():
    token = str(uuid.uuid4())
    return token


def store_refresh_token(email: str, token: str):

    token_expire = datetime.now() + timedelta(days=30)

    payload = {
        "email": email,
        "refresh_token": token,
        "created_at": datetime.now(),
        "expires_at":token_expire
    }

    refresh_tokens_collection.insert_one(payload)

    return None

def get_refresh_token(token: str):
    refresh= refresh_tokens_collection.find_one({
        "refresh_token":token
    })

    return refresh

def validate_refresh_token(refresh_token : str):
    
    found_token = refresh_tokens_collection.find_one({"refresh_token" : refresh_token})

    if not found_token:
        return None
    
    if datetime.now() > found_token["expires_at"]:
        return None
         
    return found_token

def delete_refresh_token(refresh_token : str):
    
    refresh_tokens_collection.delete_one({"refresh_token": refresh_token})

