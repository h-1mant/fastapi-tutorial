from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from typing import Dict, List, Optional

from app.models import User
from app.utils import hash
from app.schemas import UserCreate, UserResponse
from app.db_connection import SessionDep
from app.oauth2 import OAuth2Dep 

router = APIRouter()

# Get Users
@router.get("/", response_model=Dict[str, List[UserResponse]])
def get_users(session: SessionDep, token_data: OAuth2Dep, limit: int = 10, skip: int = 0, search: str | None = ""):
    try:
        stmt = select(User).filter(User.email.contains(search)).limit(limit).offset(skip)
        users = session.scalars(stmt).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Users Available")
        return {"users": users}
    except Exception:
        raise

# Create User
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, session: SessionDep):
    try:
        user.password = hash(user.password)
        user = User(**user.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        raise

# Get User
@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, session : SessionDep, token_data: OAuth2Dep):
    try:
        user = session.get(User, id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User: {id} not found")
        return user
    except Exception as e:
        raise
