from fastapi import FastAPI, HTTPException, Response, status ,Depends
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .import Model
from .database import engine ,SessionLocal
from sqlalchemy.orm import Session



Model.Base.metadata.create_all(bind=engine) #this will create the tables in our database if they do not exist already

app = FastAPI()

def get_db():# this function allows us to get a session to our database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


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

@app.get("/sqlalchemy", status_code=status.HTTP_200_OK)
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(Model.Post).all() #this will get all the posts from our database using SQLAlchemy
    return {"data": posts}

@app.get("/posts",status_code=status.HTTP_200_OK) #decorator
def get_posts():
    cursor.execute("SELECT * FROM posts") #execute the SQL statement to get all posts from the database
    posts = cursor.fetchall()
    return {"data": posts}


my_posts = [{"title": "post 1", "message": "this is post 1", "info": "this is info for post 1", "fee": 10, "id": 1},
            {"title": "post 2", "message": "this is post 2", "fee": 20, "id": 2},]


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": deleted_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *",(post.title, post.content, post.published,))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": updated_post}

