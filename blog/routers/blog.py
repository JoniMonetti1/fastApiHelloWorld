from typing import List
from fastapi import APIRouter, Depends
from .. import schemas, database
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)


@router.get("/", response_model=List[schemas.ShowAllBlogs])
def get_all_blogs(db: Session = Depends(database.get_db)):
    return blog.get_all(db)


@router.get("/{blog_id}", response_model=schemas.ShowBlog)
def get_blog_by_id(
        blog_id: int,
        db: Session = Depends(database.get_db)):
    return blog.get_by_id(blog_id, db)


@router.post("/", status_code=201)
def create_blog(request: schemas.BlogCreate, db: Session = Depends(database.get_db)):
    return blog.create(request, db)


@router.delete("/{blog_id}", status_code=204)
def delete_blog(blog_id: int, db: Session = Depends(database.get_db)):
    return blog.delete(blog_id, db)


@router.put("/{blog_id", status_code=202)
def update_blog(
        blog_id: int,
        request: schemas.BlogCreate,
        db: Session = Depends(database.get_db)):
    return blog.update(blog_id, request, db)
