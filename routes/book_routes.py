from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session as get_db
from dao import crud as crud
from typing import List

from schemas import schemas
import logging
from middlewares.auth_middleware import get_current_user

router = APIRouter()


@router.get("/books/", tags=["Books"], response_model=List[schemas.Book],status_code=status.HTTP_200_OK)
async def get_books(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        books = await crud.get_books(db, skip=skip, limit=limit)
        return books
    except Exception as e:
        logging.error(f"Book selection failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Get Books failed')


@router.get("/books/{book_id}", tags=["Books"], response_model=schemas.Book, status_code=status.HTTP_200_OK)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_book = await crud.get_book(db, book_id=book_id)
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return db_book
    except Exception as e:
        logging.error(f"Book selection failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Get Book failed')


@router.post("/books/", tags=["Books"], response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_book(db=db, book=book)
    except Exception as e:
        logging.error(f"Book insertion failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Book Creation failed')


@router.put("/books/{book_id}", tags=["Books"], response_model=schemas.Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        db_book = await crud.update_book(db=db, book_id=book_id, book=book)
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return db_book
    except Exception as e:
        logging.error(f"Book selection failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Update Book failed')


@router.delete("/books/{book_id}", tags=["Books"], response_model=schemas.Book, status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        db_book = await crud.delete_book(db=db, book_id=book_id)
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return db_book
    except Exception as e:
        logging.error(f"Book selection failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Delete Book failed')







