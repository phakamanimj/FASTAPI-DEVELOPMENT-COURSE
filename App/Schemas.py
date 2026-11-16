from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)

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
    
