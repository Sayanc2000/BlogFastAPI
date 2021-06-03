from .. import schemas, database, models
from ..hashing import Hash
from ..token import create_access_token

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Auth'],
    prefix='/auth'
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail='Not found')
    if user:
        if Hash.verify(user.password, request.password):
            access_token = create_access_token(
                data={"sub": user.email},
            )
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Invalid password")
