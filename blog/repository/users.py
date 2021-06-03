from sqlalchemy.orm import Session
from fastapi import HTTPException

from .. import schemas, models
from ..hashing import Hash


def create_user(db: Session, user: schemas.User):
    new_user = models.User(
        name=user.name, email=user.email, password=Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="not_found")
    return user
