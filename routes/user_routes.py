from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session as get_db
from dao import crud as crud
import logging
from config.auth_config import access_security
from datetime import timedelta
from schemas import schemas
from utils.utils import hash_password, verify_password

router = APIRouter()

# Define the token expiry time
TOKEN_EXPIRY_MINUTES = 30


@router.post("/users/signup", tags=["Users"], response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Check if the user already exists based on email if not create an account else return 400.
        db_user = await crud.get_user_by_email(db, email_id=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="User with the email already exists. Please proceed to Login")
        user.password = hash_password(user.password)
        return await crud.create_user(db=db, user=user)
    except Exception as e:
        logging.error(f"User Login : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Sign up failed')


@router.post("/users/login", tags=["Users"], status_code=status.HTTP_200_OK)
async def create_user(user: schemas.UserSignIn, db: AsyncSession = Depends(get_db)):
    try:
        # Check if the user already exists based on email if not create an account else return 400.
        db_user = await crud.get_user_by_email(db, email_id=user.email)
        if db_user is None:
            raise HTTPException(status_code=401, detail="User with the email does not exists. Please Sign Up !")
        elif not verify_password(plain_password=user.password, hashed_password=db_user.password):
            # elif db_user.password != user.password:
            raise HTTPException(status_code=401, detail="Incorrect Password")
        else:
            additional_claims = {
                "subject": db_user.id,
                "role": db_user.role,
                "email": db_user.email
            }
            expires_delta = timedelta(minutes=TOKEN_EXPIRY_MINUTES)
            access_token = access_security.create_access_token(subject=additional_claims, expires_delta=expires_delta)
        logging.info(f"Token Generated : {access_token} for {db_user.email}")
        return {"access_token": f'{access_token}'}
    except Exception as e:
        logging.error(f"User Login : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Login failed')


# @router.post("/users/", tags=["Users"], response_model=schemas.User)
# async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
#     return await crud.create_user(db=db, user=user)
#
#
# @router.get("/users/{user_id}", tags=["Users"], response_model=schemas.User)
# async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     db_user = await crud.get_user_by_id(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @router.put("/users/{user_id}", tags=["Users"], response_model=schemas.User)
# async def update_user(user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
#     db_user = await crud.update_user(db=db, user_id=user_id, user=user)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @router.delete("/users/{user_id}", tags=["Users"], response_model=schemas.User)
# async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     db_user = await crud.delete_user(db=db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @router.get("/users/", tags=["Users"], response_model=List[schemas.User])
# async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
#     users = await crud.get_users(db, skip=skip, limit=limit)
#     return users
