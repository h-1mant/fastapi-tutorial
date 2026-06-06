
from typing import Dict, List
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.schemas import PostResponse, PostCreate, PostUpdate
from app.models import Post
from app.db_connection import SessionDep
from app.oauth2 import OAuth2Dep

router = APIRouter()

# Get All Posts
@router.get("/", response_model=Dict[str, List[PostResponse]])
def get_posts(session: SessionDep, token_data: OAuth2Dep, limit: int = 10, skip: int = 0, search: str | None = ""):
    try:        
        stmt = select(Post).filter(Post.title.contains(search)).limit(limit).offset(skip)
        posts = session.scalars(stmt).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Posts Available")
        return {"posts": posts}
    except Exception:
        raise

# Get User's Posts
@router.get("/my_posts", response_model=Dict[str, List[PostResponse]])
def get_my_posts(session: SessionDep, token_data: OAuth2Dep, limit: int = 10, skip: int = 0, search: str | None = ""):
    try:
        stmt = select(Post).where(Post.user_id == token_data.id).filter(Post.title.contains(search)).limit(limit).offset(skip)
        posts = session.scalars(stmt).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You don't have any posts")
        return {"posts": posts}
    except Exception:
        raise

# Get Post at ID
@router.get("/{id}", response_model=PostResponse)
def get_posts(id: int, session: SessionDep, token_data: OAuth2Dep):
    try:
        post = session.get(Post, id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post {id} not found")
        return post
    except Exception:
        raise

# Create Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, session: SessionDep, token_data: OAuth2Dep):
    try:
        post.user_id = token_data.id
        new_post = Post(**post.model_dump())
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))
    

# Update User's Post
@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: PostUpdate, session: SessionDep, token_data: OAuth2Dep):
    try:
        post = session.scalars(select(Post).where(Post.id == id, Post.user_id == token_data.id)).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your Post: {id} not found")
        
        for field, value in updated_post.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        
        post.updated_ts = datetime.now(timezone.utc)
        session.commit()
        session.refresh(post)
        return post
    except Exception:
        raise 

# Delete User's Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: SessionDep, token_data: OAuth2Dep):
    post = session.scalars(select(Post).where(Post.id == id, Post.user_id == token_data.id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your Post: {id} not found")
    session.delete(post)
    session.commit()