from pydantic import BaseModel

class Blog(BaseModel):
    body: str
    title: str
