from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
from app.schemas import TokenData
from fastapi.security import OAuth2PasswordBearer

# this just extracts the Bearer token from Authorization header
# so that `get_current_user` can receive it to call `verify_access_token`
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    to_encode.update({"exp": exp})
    
    token = jwt.encode(claims=to_encode, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])

        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        
        token = TokenData(id=id)
        return token
    except JWTError:
        raise credentials_exception

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_access_token(token, credentials_exception)


# Create an OAuth2 Dependency to protect endpoints
OAuth2Dep = Annotated[TokenData, Depends(get_current_user)]

def _auth_headers(user_id: int = 1):
    """helper function to bypass login functionality by adding a dummy Authorization header"""
    token = create_access_token({"user_id": user_id})
    return {"Authorization": f"Bearer {token}"}








