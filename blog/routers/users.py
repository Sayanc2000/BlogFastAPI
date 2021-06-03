from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from ..database import get_db
from ..hashing import Hash
from .. import models, schemas
from ..repository import users

from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Users'],
    prefix='/users'
)


@router.post("/new", response_model=schemas.ShowUser)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return users.create_user(db, user)


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return users.get_user_by_id(db, id)
