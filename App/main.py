from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
while True:# this while loop will continously run until we connect to our database successfully, if we fail to connect it will wait for 2 seconds and try again
    try:
        conn = psycopg2.connect(host='localhost', database='Fast API Database', user='postgres', password='Maboni123#', cursor_factory=RealDictCursor )#we are coonecting to our database
        cursor = conn.cursor() #we use this to execute SQL ststements
        print("DATABASE SUCCEFULLY CONNECTED")
        break
    except Exception as error:
        print("DATABASE CONNECTION FAILED")
        print("Error: ", error)
        time.sleep(2) #wait for 2 seconds before trying to connect again

@app.get("/posts") #decorator
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


my_posts = [{"title": "post 1", "message": "this is post 1", "info": "this is info for post 1", "fee": 10, "id": 1},
            {"title": "post 2", "message": "this is post 2", "fee": 20, "id": 2},]


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        return {"message": "post not found"}
    return {"data": post}

@app.delete("/posts/{id}")
def delete_post(id :int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        return {"message": "post not found"}
    return {"data": deleted_post}

@app.post("/posts")
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *",(post.title, post.content, post.published,))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}