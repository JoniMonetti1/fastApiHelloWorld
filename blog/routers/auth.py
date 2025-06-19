from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm

from ..JWT import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..hashing import Hash
from fastapi import APIRouter, Depends, HTTPException
from .. import models, database
from sqlalchemy.orm import Session

from ..schemas import Token

router = APIRouter(
    tags=["auth"]
)

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code = 401, detail= "Invalid credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code = 401, detail= "Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

