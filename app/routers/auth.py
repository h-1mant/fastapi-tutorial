from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import EmailStr
from app.db_connection import SessionDep
from app.models import User
from app.schemas import TokenResponse
from app.utils import hash, verify_hash
from app.oauth2 import create_access_token
from sqlalchemy import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter()

@router.post("/", response_model = TokenResponse)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    try:
        user = session.scalars(select(User).where(User.email == user_credentials.username)).first()
        if not user:
            raise HTTPException(403, "Invalid Credentials")
        if not verify_hash(user_credentials.password, user.password):
            raise HTTPException(403, "Invalid Credentials")

        access_token = create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception:
        raise
        
        
        

 
    
