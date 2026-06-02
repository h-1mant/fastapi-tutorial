from app.models import Base
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

engine = create_engine(os.getenv("CONN_STRING"))

# commenting below since alembic now handles DB migrations
Base.metadata.create_all(engine)

def get_session():
    try:
        session = Session(bind=engine, autocommit=False)
        yield session
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]