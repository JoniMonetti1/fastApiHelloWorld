from typing import List
from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)


@router.get("/", response_model=List[schemas.ShowAllBlogs])
def get_all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{blog_id}", response_model=schemas.ShowBlog)
def get_blog_by_id(
        blog_id: int,
        db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id:{blog_id} not found")
    return blog


@router.post("/", status_code=201)
def create_blog(request: schemas.BlogCreate, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{blog_id}", status_code=204)
def delete_blog(blog_id: int, db: Session = Depends(database.get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id:{blog_id} not found")

    blog_query.delete(synchronize_session=False)

    db.commit()

    return {"detail": f"Blog with id:{blog_id} deleted successfully"}


@router.put("/{blog_id", status_code=202)
def update_blog(
        blog_id: int,
        request: schemas.BlogCreate,
        db: Session = Depends(database.get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id:{blog_id} not found")

    blog_query.update(request.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(blog)

    return blog
