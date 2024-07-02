from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
access_security = JwtAccessBearer(secret_key="SECRET", auto_error=True)


# from pydantic import BaseModel, Field, validator
# from fastapi_jwt_auth import AuthJWT
# from datetime import timedelta
# from typing import Set
#
#
# class Settings(BaseModel):
#     # authjwt_secret_key: str = "asdfgh"
#     authjwt_secret_key: str = Field("asdfgh", alias="authjwt_secret_key")
#     # authjwt_token_location: Set[str] = {'headers'}   # 'cookies' can be added. searches for token in Authorization header
#     # authjwt_access_token_expires: int = 60*60*12  # in seconds, 12hrs expiry
#     # authjwt_refresh_token_expires: timedelta = timedelta(days=30)
#
#     @validator('authjwt_secret_key')
#     def check_secret_key(cls, v):
#         if not v or len(v) < 6:
#             raise ValueError('authjwt_secret_key must be at least 6 characters long')
#         return v
#
#
# @AuthJWT.load_config
# def get_config():
#     return Settings()
#
#
#
