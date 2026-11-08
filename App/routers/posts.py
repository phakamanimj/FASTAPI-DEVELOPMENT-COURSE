from fastapi import FastAPI, HTTPException, Response, status ,Depends ,APIRouter 
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import time
from ..import Model,Schemas,Database_Connection

router = APIRouter()


@router.get("/posts",status_code=status.HTTP_200_OK) #decorator
def get_posts():
    Database_Connection.cursor.execute("SELECT * FROM posts") #execute the SQL statement to get all posts from the database
    post = Database_Connection.cursor.fetchall()
    return post


@router.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int,post: Schemas.Post):
    Database_Connection.cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = Database_Connection.cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post 


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    Database_Connection.cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    Database_Connection.conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return  deleted_post


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Schemas.Post):
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *",(new_post.title, new_post.content, new_post.published,))
    new_post = Database_Connection.cursor.fetchone()
    Database_Connection.conn.commit()
    return  new_post

@router.put("/posts/{id}")
def update_post(id: int, post: Schemas.Post):
    Database_Connection.cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    updated_post = Database_Connection.cursor.fetchone()
    Database_Connection.conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": updated_post}



