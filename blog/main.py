from fastapi import FastAPI, Depends, Response, HTTPException

from . import schemas, models
from .database import engine, SessionLocal

from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/blog", status_code = 201)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{blog_id}", status_code = 204)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code = 404, detail = f"Blog with id:{blog_id} not found")

    blog_query.delete(synchronize_session=False)

    db.commit()

    return {"detail": f"Blog with id:{blog_id} deleted successfully"}

@app.put("/blog/{blog_id", status_code = 202)
def update_blog(
        blog_id: int,
        request: schemas.Blog,
        db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code = 404, detail = f"Blog with id:{blog_id} not found")

    blog_query.update(request.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(blog)

    return blog

@app.get("/blog")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{blog_id}", status_code = 200)
def get_blog_by_id(
        blog_id: int,
        response: Response,
        db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code = 404, detail = f"Blog with id:{blog_id} not found")
        # response.status_code = 404
        # return {"error": f"Blog with id:{blog_id} not found"}
    return blog
