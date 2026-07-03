from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, UTC, timedelta
from env_config import settings
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data: dict) -> str :
    payload = data.copy()
    expires_in = datetime.now(UTC) + timedelta(minutes=settings.expiry)
    payload.update({"exp" : expires_in})
    
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token


def verify_token(token: str, credentials_exception) -> int :
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if not payload:
            raise credentials_exception

        user_id = payload.get("id")
        if not user_id:
            raise credentials_exception
        
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired. Please log in again")
        
    except JWTError:
        raise credentials_exception
    
    return user_id

def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return verify_token(token, credentials_exception)