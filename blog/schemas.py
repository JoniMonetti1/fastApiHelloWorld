from pydantic import BaseModel
from typing import List, Optional


# ---------- USER SCHEMAS ----------

class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class ShowUser(UserBase):
    class Config:
        from_attributes = True


# ---------- BLOG SCHEMAS ----------

class BlogBase(BaseModel):
    title: str
    body: str


class BlogCreate(BlogBase):
    pass


class ShowBlog(BlogBase):
    creator: ShowUser

    class Config:
        from_attributes = True


class ShowAllBlogs(BaseModel):
    id: int
    title: str
    creator: ShowUser

    class Config:
        from_attributes = True


# ---------- USER WITH BLOGS ----------

class ShowUserWithBlogs(ShowUser):
    blogs: List[ShowAllBlogs]

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None