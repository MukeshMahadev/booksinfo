from pydantic import BaseModel, ConfigDict
from typing import Sequence, Union
from typing import List

# Reviews Schema

# If I want to create a schema for adding review for a book what will  I need
# user_id => from Authorization code = A Middleware will populate it from Auth token.
# book_id
# review string


class ReviewBase(BaseModel):
    book_id: int
    review: str


class ReviewsCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)


# Books Schema
class BookBase(BaseModel):
    title: str
    isbn: str
    author: str
    genre: str | None = None
    year_published: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    summary: str

    model_config = ConfigDict(from_attributes=True)


class BookList(BaseModel):
    books: List[Book]

    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    year_published: int | None = None



