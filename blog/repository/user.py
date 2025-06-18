from fastapi import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..hashing import Hash

def get_by_id(
        user_id: int,
        db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = f"User with id: {user_id} not found")

    return user

def create(request: schemas.UserCreate, db: Session):
    new_user = models.User(username = request.username, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user