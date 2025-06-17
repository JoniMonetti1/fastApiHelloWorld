from pydantic import BaseModel

class Blog(BaseModel):
    body: str
    title: str

class ShowBlog(Blog):
    class Config:
         from_attributes = True

class ShowAllBlogs(BaseModel):
    title: str
    id: int

    class Config:
        from_attributes = True

class User(BaseModel):
    username: str
    email: str
    password: str



