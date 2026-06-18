from pydantic import BaseModel

class User_Info(BaseModel):
    name: str
    account_created: str
    flag : bool