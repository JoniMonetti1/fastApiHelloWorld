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


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
