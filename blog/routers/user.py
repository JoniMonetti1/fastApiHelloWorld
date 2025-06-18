from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from ..hashing import Hash


router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.get("/{user_id}", response_model =  schemas.ShowUser)
def get_user_by_id(
        user_id: int,
        db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = f"User with id:{user_id} not found")

    return user

@router.post("/", response_model = schemas.UserCreate, status_code = 201)
def create_user(request: schemas.UserCreate, db: Session = Depends(database.get_db)):
    new_user = models.User(username = request.username, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user