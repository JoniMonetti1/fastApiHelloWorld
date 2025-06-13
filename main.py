from fastapi import FastAPI

app = FastAPI()


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

@app.get("/blog/{id}")
def get_blog(id: int):
    return {
        "data": {
            "blog": id
        }
    }


@app.get("/blogs")
def get_all_blogs(limit: int = 10, published: bool = True):
    if published:
        return {
            "data": [
                {"title": "Blog 1", "content": "Content of blog 1"},
                {"title": "Blog 2", "content": "Content of blog 2"}
            ],
            "message": f"Showing {limit} blogs"
        }
    else:
        return {
            "data": [
                {"title": "Blog 3", "content": "Content of blog 3"},
                {"title": "Blog 4", "content": "Content of blog 4"}
            ],
            "message": f"Showing {limit} blogs"
        }
