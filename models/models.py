from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


# declarative base class
class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    isbn: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    genre: Mapped[str] = mapped_column(String)
    year_published: Mapped[int] = mapped_column(Integer)
    summary: Mapped[str] = mapped_column(String)

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="book", lazy="joined")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    review_text: Mapped[str] = mapped_column(String)
    rating: Mapped[int] = mapped_column(Integer)

    book: Mapped["Book"] = relationship("Book", back_populates='reviews', lazy="joined")
    user: Mapped["User"] = relationship("User")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, nullable=True)


# # Define a simple model (replace with your actual model structure)
# class Book(Base):
#     __tablename__ = "books"
#
#     # id, title, author, genre, year_published, summary.
#     id = Column(Integer, primary_key=True, unique=True)  # auto created while inserting into db
#     isbn = Column(String, unique=True)  # isbn is global
#     title = Column(String)  # title can be same for two books
#     author = Column(String)
#     genre = Column(String)
#     year_published = Column(Integer)
#     summary = Column(String)
#
#     reviews = relationship("Review", back_populates="book", lazy="joined")
#
#
# class Review(Base):
#     __tablename__ = "reviews"
#
#     # id, book_id (foreign keyreferencing books), user_id, review_text, rating.
#     id = Column(Integer, primary_key=True)
#     book_id = Column(Integer, ForeignKey("books.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))
#     review_text = Column(String)
#     rating = Column(Integer)
#     book = relationship("Book", back_populates='reviews', lazy="joined")
#     user = relationship("User")
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     # id, title, author, genre, year_published, summary.
#     id = Column(Integer, primary_key=True)
#     email = Column(String)
#     password = Column(String)
#     name = Column(String)
