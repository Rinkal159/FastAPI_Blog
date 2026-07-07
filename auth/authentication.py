from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, UTC, timedelta
from env_config import settings
from fastapi import status, Cookie
from utils.exception import raise_exception


def create_token(data: dict) -> str :
    payload = data.copy()
    expires_in = datetime.now(UTC) + timedelta(minutes=settings.expiry)
    payload.update({"exp" : expires_in})
    
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token


def verify_token(token: str) -> int :
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        
        user_id = payload.get("id")
        
        if not user_id:
            raise raise_exception(status.HTTP_401_UNAUTHORIZED, "Invalid token")
        
    except ExpiredSignatureError:
        raise raise_exception(status.HTTP_401_UNAUTHORIZED, "Session is expired. Please log in again.")
        
    except JWTError:
        raise raise_exception(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    
    
    return user_id

def get_current_user(access_token: str | None = Cookie(None)):
    if access_token is None:
            raise raise_exception(status.HTTP_401_UNAUTHORIZED, "Session is expired. Please log in again.")
        
    return verify_token(access_token)