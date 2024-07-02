from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.models import Book  # Assuming Book model is defined elsewhere
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError

from old.schemas_old import BookCreate, BookUpdate

from sqlalchemy.orm import joinedload


# Function to get a book by ISBN using AsyncSession
async def get_book_by_isbn(session: AsyncSession, isbn: str) -> Optional[Book]:
    async with session.begin():
        stmt = select(Book).where(Book.isbn == isbn)
        result = await session.execute(stmt)
        book = result.scalars().first()
        return book


# Function to get a book by ISBN using AsyncSession
async def get_book_by_id(session: AsyncSession, book_id: str) -> Optional[Book]:
    async with session.begin():
        stmt = select(Book).where(Book.id == book_id)
        result = await session.execute(stmt)
        book = result.scalars().first()
        return book


async def get_all_books(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Book]:
    books = []
    async with session.begin():
        stmt = select(Book).options(joinedload(Book.reviews)).offset(skip).limit(limit)
        result = await session.execute(stmt)
        books = result.scalars().unique().all()
        # # Explicitly load all attributes if necessary
        # for book in books:
        #     # Access the attributes to ensure they are loaded
        #     _ = book.title, book.isbn, book.author, book.genre, book.year_published, book.summary

    return books


async def get_books(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Book]:
    """Asynchronously retrieves a list of users from the database with pagination.

    Args:
        session: The asynchronous database session.
        skip: Number of users to skip (for pagination). Defaults to 0.
        limit: Maximum number of users to retrieve. Defaults to 100.

    Returns:
        A list of User objects.
    """
    try:
        # Construct a select query
        query = select(Book).offset(skip).limit(limit)

        # Execute the query asynchronously
        result = await session.execute(query)

        # Fetch results as Book objects
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise


# Function to insert a new book using AsyncSession
async def add_book(session: AsyncSession, book: BookCreate) -> Book:
    async with session.begin():
        new_book = Book(**book.dict())
        session.add(new_book)
        await session.commit()
        return new_book


async def update_book(session: AsyncSession, book_id: int, book_data: BookUpdate) -> Optional[Book]:
    """Asynchronously updates a book in the database partially or fully.

    Args:
        session: The asynchronous database session.
        book_id: The ID of the book to update.
        book_data: The data to be updated (schemas.BookCreate).

    Returns:
        The updated book object if found, otherwise None.

    Raises:
        ValueError: If both title and author are None in book_data.
    """



    # Get the book object by ID
    book = await session.get(Book, book_id)
    if not book:
        return None

    # Update attributes using setter methods (if defined)
    if book_data.title:
        book.title = book_data.title
    if book_data.author:
        book.author = book_data.author
    if book_data.genre:
        book.author = book_data.genre
    if book_data.year_published:
        book.author = book_data.year_published
    # Add similar lines for genre and year_published if needed

    # Commit the changes
    session.add(book)  # Mark the object as dirty for update
    await session.commit()

    return book
