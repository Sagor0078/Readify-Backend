from pydantic import BaseModel, Field
from datetime import datetime
from src.books.schemas import Book
from typing import List
import uuid


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=40)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(max_length=6)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    password_hash: str = Field(exclude=True)
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserBooksModel(UserModel):
    books: List[Book]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(max_length=6)
