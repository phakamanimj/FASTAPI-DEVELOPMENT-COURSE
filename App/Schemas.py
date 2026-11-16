from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
   # owner: UserOut


class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class Userlogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
