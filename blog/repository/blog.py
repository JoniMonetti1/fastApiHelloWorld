from fastapi import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def get_by_id(
        blog_id: int,
        db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id:{blog_id} not found")
    return blog

def create(request: schemas.BlogCreate, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(blog_id: int, db: Session):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id:{blog_id} not found")

    blog_query.delete(synchronize_session=False)

    db.commit()

    return {"detail": f"Blog with id:{blog_id} deleted successfully"}

def update(
        blog_id: int,
        request: schemas.BlogCreate,
        db: Session):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id:{blog_id} not found")

    blog_query.update(request.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(blog)

    return blog