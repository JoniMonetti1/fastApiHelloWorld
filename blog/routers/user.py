from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, database
from ..Oauth2 import get_current_user
from ..repository import user


router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.get("/{user_id}", response_model =  schemas.ShowUser)
def get_user_by_id(
        user_id: int,
        db: Session = Depends(database.get_db),
        current_user: schemas.TokenData = Depends(get_current_user)):
    return user.get_by_id(user_id, db)

@router.post("/", response_model = schemas.UserCreate, status_code = 201)
def create_user(request: schemas.UserCreate,
                db: Session = Depends(database.get_db),
                current_user: schemas.TokenData = Depends(get_current_user)):
    return user.create(request, db)