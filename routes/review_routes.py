from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session as get_db
from dao import crud as crud

from schemas import schemas
from middlewares.auth_middleware import get_current_user
import logging

router = APIRouter()


@router.post("/reviews/", tags=["Reviews"], response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
async def create_review(review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        return await crud.create_review(db=db, review=review)
    except Exception as e:
        logging.error(f"Review insertion failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Review Creation failed')


@router.get("/reviews/{review_id}", tags=["Reviews"], response_model=schemas.Review, status_code=status.HTTP_200_OK)
async def read_review(review_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_review = await crud.get_review(db, review_id=review_id)
        if db_review is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return db_review
    except Exception as e:
        logging.error(f"Review read failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Review read failed')


@router.put("/reviews/{review_id}", tags=["Reviews"], response_model=schemas.Review, status_code=status.HTTP_200_OK)
async def update_review(review_id: int, review: schemas.ReviewUpdate, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        # TODO: check the created user - only he should be able to update.
        db_review = await crud.update_review(db=db, review_id=review_id, review=review)
        if db_review is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return db_review
    except Exception as e:
        logging.error(f"Review update failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Review Update failed')


@router.delete("/reviews/{review_id}", tags=["Reviews"], response_model=schemas.Review, status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        # TODO: check the created user - only he should be able to update.
        db_review = await crud.delete_review(db=db, review_id=review_id)
        if db_review is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return db_review
    except Exception as e:
        logging.error(f"Review deletion failed : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Review Creation failed')

