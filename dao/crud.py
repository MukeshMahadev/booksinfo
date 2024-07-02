from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from models.models import Book, Review, User
from schemas.schemas import BookCreate, BookUpdate, ReviewCreate, ReviewUpdate, UserCreate, UserUpdate

"""################################# Books CRUD functions #######################################"""


async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(Book).filter(Book.id == book_id).options(joinedload(Book.reviews)))
    return result.scalars().first()


async def create_book(db: AsyncSession, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def update_book(db: AsyncSession, book_id: int, book: BookUpdate):
    db_book = await get_book(db, book_id)
    if db_book:
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        await db.commit()
        await db.refresh(db_book)
        return db_book
    return None


async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    if db_book:
        await db.delete(db_book)
        await db.commit()
    return db_book


async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Book).options(joinedload(Book.reviews)).offset(skip).limit(limit))
    return result.scalars().unique().all()


"""################################# Review CRUD functions #######################################"""


async def get_review(db: AsyncSession, review_id: int):
    result = await db.execute(select(Review).filter(Review.id == review_id))
    return result.scalars().first()


async def create_review(db: AsyncSession, review: ReviewCreate):
    db_review = Review(**review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review


async def update_review(db: AsyncSession, review_id: int, review: ReviewUpdate):
    db_review = await get_review(db, review_id)
    if db_review:
        for key, value in review.dict().items():
            setattr(db_review, key, value)
        await db.commit()
        await db.refresh(db_review)
        return db_review
    return None


async def delete_review(db: AsyncSession, review_id: int):
    db_review = await get_review(db, review_id)
    if db_review:
        await db.delete(db_review)
        await db.commit()
    return db_review

"""################################# User CRUD functions #######################################"""


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email_id: str):
    result = await db.execute(select(User).filter(User.email == email_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user: UserUpdate):
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    return None


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

