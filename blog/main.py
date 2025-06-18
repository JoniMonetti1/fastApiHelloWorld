from fastapi import FastAPI, Depends, Response, HTTPException

from typing import List

from . import schemas, models
from .database import engine, SessionLocal

from sqlalchemy.orm import Session
from .hashing import Hash
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/blog", status_code = 201, tags=["blogs"])
def create_blog(request: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{blog_id}", status_code = 204, tags=["blogs"])
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code = 404, detail = f"Blog with id:{blog_id} not found")

    blog_query.delete(synchronize_session=False)

    db.commit()

    return {"detail": f"Blog with id:{blog_id} deleted successfully"}

@app.put("/blog/{blog_id", status_code = 202, tags=["blogs"])
def update_blog(
        blog_id: int,
        request: schemas.BlogCreate,
        db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code = 404, detail = f"Blog with id:{blog_id} not found")

    blog_query.update(request.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(blog)

    return blog

@app.get("/blog", response_model = List[schemas.ShowAllBlogs], tags=["blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{blog_id}",response_model = schemas.ShowBlog, tags=["blogs"])
def get_blog_by_id(
        blog_id: int,
        db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code = 404, detail = f"Blog with id:{blog_id} not found")
        # response.status_code = 404
        # return {"error": f"Blog with id:{blog_id} not found"}
    return blog

@app.post("/user", response_model = schemas.UserCreate, status_code = 201, tags=["User"])
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(username = request.username, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{user_id}", response_model =  schemas.ShowUser, tags=["User"])
def get_user_by_id(
        user_id: int,
        db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = f"User with id:{user_id} not found")

    return user


