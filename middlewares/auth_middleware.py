from fastapi import Depends, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials

from jwt import PyJWT

from config.auth_config import access_security


async def get_current_user(credentials: JwtAuthorizationCredentials = Depends(access_security)):
    try:
        user = credentials.subject
        return user
    except PyJWT.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid token")


# Optionally, you can create another dependency for roles
# def get_current_active_user(user: dict = Depends(get_current_user)):
#     if user.get("role") != "active_user_role":
#         raise HTTPException(status_code=403, detail="Inactive user")
#     return user
