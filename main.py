from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.get("/")
def index():
    return {
        "data": {
            "message": "Hello World!"
        }
    }

@app.get("/about")
def about():
    return {
        "data": {
            "message": "This is the About page"
        }
    }

@app.get("/hola/{hola_luchi}")
def first_home(hola_luchi: str):
    return {
        "data": {
            "message": f"Hello {hola_luchi}"
        }
    }


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/blog")
def get_blogs(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {
            "data": f"{limit} published blogs from the database"
        }
    else:
        return {
            "data": f"{limit} blogs from the database"
        }


@app.post("/blog")
def create_blog(blog: Blog):
    return {
        "data": {
            "title": blog.title,
            "body": blog.body,
            "published": blog.published
        }
    }

@app.post("/blogs")
def create_blogs(blog: Blog):  # Changed function name
    return {
        "data": {
            "title": blog.title,
            "body": blog.body,
            "published": blog.published
        }
    }
