from pydantic import BaseModel,EmailStr

from typing import Optional

class User(BaseModel):
    username: Optional[str]= None
    email : Optional[EmailStr] = None
    full_name : Optional[str] = None
    disabled: Optional[bool] = None

class UserCreate(User):
    password: str

class UserInDB(User):
    hashed_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str