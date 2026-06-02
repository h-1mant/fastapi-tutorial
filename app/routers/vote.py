from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from typing import Dict, List, Optional

from app.models import User, Post, Vote
from app.utils import hash
from app.schemas import VoteCreate, VoteResponse
from app.db_connection import SessionDep
from app.oauth2 import OAuth2Dep 

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VoteResponse)
def vote(vote: VoteCreate, session: SessionDep, token_data: OAuth2Dep):
    try:
        # Find the post
        post = session.scalars(select(Post).filter(Post.id == vote.post_id)).first()
        if not post:
            raise HTTPException(404, f"Post {vote.post_id} does not exist")
        
        # Check existing Vote Status of (User, Post)
        existing_vote = session.scalars(select(Vote).filter(Vote.user_id == token_data.id).filter(Vote.post_id == post.id)).first()

        if existing_vote and vote.vote_dir == 1:
            raise HTTPException(400,"You already voted on this post")
        if not existing_vote and vote.vote_dir == 0:
            raise HTTPException(400,"You haven't voted on this post")
        
        # Create Vote
        if vote.vote_dir == 1:
            new_vote = Vote(user_id=token_data.id, post_id = post.id)
            session.add(new_vote)
            session.commit()
            session.refresh(new_vote)
        # Remove Vote
        else:
            session.delete(existing_vote)
            session.commit()
        
        # Update total Vote count for post
        if vote.vote_dir == 1:
            post.votes += 1
        else:
            post.votes -= 1        
        session.commit()
        session.refresh(post)

        return {"post_id": post.id, "vote_dir": vote.vote_dir}
    except Exception as e:
        raise 



    


