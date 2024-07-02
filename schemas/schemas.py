from pydantic import BaseModel
from typing import Optional, List


class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    genre: str
    year_published: int
    summary: str


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    reviews: List["Review"] = []

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    book_id: int
    user_id: int
    review_text: str
    rating: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    password: str
    name: str


class UserCreate(UserBase):
    role: str = 'user'
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserSignIn(BaseModel):
    email: str
    password: str
