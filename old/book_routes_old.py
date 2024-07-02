import logging

from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import schemas
from db.database import get_session
from old import booksdao

router = APIRouter()


@router.post("/books/")
async def add_book(book: schemas.BookCreate, session: AsyncSession = Depends(get_session)):
    try:
        # Check if the book with same ibn exists in the db
        db_book = await booksdao.get_book_by_isbn(session, isbn=book.isbn)
        if db_book:
            raise HTTPException(status_code=400, detail="Book with the given ISBN already exists")
        new_book = await booksdao.add_book(session=session, book=book)
        return new_book
    except Exception as e:
        logging.error(f"Book insertion failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Book Insertion failed')


@router.get("/books/")
async def get_books(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    try:
        books = await booksdao.get_all_books(session=session, skip=skip, limit=limit)
        # return schemas.BookList(books=books)
        books_r = []
        for book in books:
            temp_book = {
                "book_id": book.id,
                "title": book.title
            }
            books_r.append(temp_book)
        # return [schemas.Book.from_orm(book) for book in books]
        return books_r
    except Exception as e:
        logging.error(f"Book insertion failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Get Books failed')


@router.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, session: AsyncSession = Depends(get_session)):
    db_book = booksdao.get_book_by_id(session, id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.post("/books", response_model=schemas.BookCreate)
async def update_book(book: schemas.BookUpdate, session: AsyncSession = Depends(get_session)):
    try:
        print("in books")
        if not book.title and not book.author and not book.genre and not book.year_published:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field must be provided for update.")
        # Check if the book with same ibn exists in the db
        updated_db_book = booksdao.update_book(session, isbn=book)
        return updated_db_book
    except Exception as e:
        logging.error(f"Book insertion failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Audio Combine Failed')
