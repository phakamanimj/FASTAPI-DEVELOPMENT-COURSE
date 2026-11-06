from fastapi import FastAPI, HTTPException, Response, status ,Depends ,APIRouter 
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from ..import Model,Schemas

router = APIRouter()

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

@router.get("/posts",status_code=status.HTTP_200_OK) #decorator
def get_posts():
    cursor.execute("SELECT * FROM posts") #execute the SQL statement to get all posts from the database
    post = cursor.fetchall()
    return post


@router.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int,post: Schemas.Post):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post 


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return  deleted_post


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Schemas.Post):
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *",(new_post.title, new_post.content, new_post.published,))
    new_post = cursor.fetchone()
    conn.commit()
    return  new_post

@router.put("/posts/{id}")
def update_post(id: int, post: Schemas.Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": updated_post}



