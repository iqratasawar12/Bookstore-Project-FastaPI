from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID
from datetime import date
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    DOB: date
    gender: GenderEnum
    country: str
    email: EmailStr

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: UUID

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    category_name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: UUID

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    description: str
    author_id: UUID

class BookCreate(BookBase):
    # category_ids: List[UUID]
    category_ids: Optional[List[UUID]] = []

class Book(BookBase):
    id: UUID
    author: Author
    categories: List[Category] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr
    disabled: Optional[bool] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True

class UserInDB(UserBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

