from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    Message: str
    info:str = "this is a default info"
    fee:int = 0

@app.get("/") #decorator
async def root():
    return {"message": "Hello Phakamani welcome to FastAPI!"}


@app.post("/posts")
def create_posts(post: Post):
    print(post)
    return "Successfully created post with title: {} and message: {}".format(post.title, post.Message)
