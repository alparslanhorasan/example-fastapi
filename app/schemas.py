from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# pydantic için
class PostBase(BaseModel):
    title: str
    content:str
    published: bool=True

class PostCreate(PostBase):
    pass

# Response Schema
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Post Modelini inherit'li yapalım
class Post(PostBase):
    id: int
    created_at: datetime
    # users ve posts arasındaki relation'dan sonra eklendi
    owner_id: str
    # SQLAlchemy Relation için
    owner: UserOut
    
    class Config:
        orm_mode = True

# JOIN'lu sorgu içinhazırladık
class PostOut(BaseModel):
    Post: Post
    votes: int

# inherit'siz hali
# class Post(BaseModel):
#     id: int
#     title: str
#     content:str
#     published: bool
#     created_at: datetime
    
#     class Config:
#         orm_mode = True

# User İşlemleri
# Request Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    #dir: int
    dir: conint(le=1)
