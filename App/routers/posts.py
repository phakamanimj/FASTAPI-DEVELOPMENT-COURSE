from fastapi import FastAPI, HTTPException, Response, status ,Depends ,APIRouter 
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import time

from App import Auth2
from ..import Model,Schemas,Database_Connection

router = APIRouter()


@router.get("/posts",status_code=status.HTTP_200_OK,response_model=list[Schemas.PostOut]) #decorator
def get_posts():
    # JOIN the users table so every post comes back with its owner's details
    Database_Connection.cursor.execute("""SELECT posts.*,json_build_object('id', users.id, 'name', users.name, 'email', users.email) AS owner FROM posts JOIN users ON posts.user_id = users.id""")
    post = Database_Connection.cursor.fetchall()
    return post

@router.get("/getmy_posts",status_code=status.HTTP_200_OK,response_model=list[Schemas.PostOut])
def getmy_posts(current_user: Schemas.TokenData = Depends(Auth2.get_current_user)):
  Database_Connection.cursor.execute("""
      SELECT posts.*,
             json_build_object('id', users.id, 'name', users.name, 'email', users.email) AS owner
      FROM posts
      JOIN users ON posts.user_id = users.id
      WHERE posts.user_id = %s
  """, (int(current_user.id),))
  posts = Database_Connection.cursor.fetchall()
  return posts


@router.get("/posts/{id}", status_code=status.HTTP_200_OK,response_model=Schemas.PostOut)
def get_post(id: int):
    Database_Connection.cursor.execute("""
        SELECT posts.*,
               json_build_object('id', users.id, 'name', users.name, 'email', users.email) AS owner
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = %s
    """, (id,))
    post = Database_Connection.cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.get("/getpost/{id}",status_code=status.HTTP_200_OK,response_model=Schemas.PostOut)
def get_my_post(id :int,current_user: Schemas.TokenData=Depends(Auth2.get_current_user)):
    Database_Connection.cursor.execute("""
        SELECT posts.*,
               json_build_object('id', users.id, 'name', users.name, 'email', users.email) AS owner
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = %s
    """, (id,))
    post = Database_Connection.cursor.fetchone()

    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "post not Found")

    if int(current_user.id) != post["user_id"]:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to get this post")
    return post
      
    


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user: Schemas.TokenData = Depends(Auth2.get_current_user)):
    Database_Connection.cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = Database_Connection.cursor.fetchone()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post["user_id"] != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    Database_Connection.cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    Database_Connection.conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Schemas.PostOut)
def create_posts(new_post: Schemas.PostCreate, get_current_user: int = Depends(Auth2.get_current_user)):
    # The CTE ("WITH inserted AS ...") inserts the row, then the SELECT joins it to users
    # so the response also contains the owner.
    Database_Connection.cursor.execute("""
        WITH inserted AS (
            INSERT INTO posts (title, content, published, user_id)
            VALUES (%s, %s, %s, %s)
            RETURNING *
        )
        SELECT inserted.*,
               json_build_object('id', users.id, 'name', users.name, 'email', users.email) AS owner
        FROM inserted
        JOIN users ON inserted.user_id = users.id
    """, (new_post.title, new_post.content, new_post.published, int(get_current_user.id)))
    created_post = Database_Connection.cursor.fetchone()
    Database_Connection.conn.commit()
    return created_post

@router.put("/posts/{id}", response_model=Schemas.PostOut)
def update_post(id: int, post: Schemas.PostCreate, get_current_user: int = Depends(Auth2.get_current_user)):
    Database_Connection.cursor.execute("""
        WITH updated AS (
            UPDATE posts SET title = %s, content = %s, published = %s
            WHERE id = %s
            RETURNING *
        )
        SELECT updated.*,
               json_build_object('id', users.id, 'name', users.name, 'email', users.email) AS owner
        FROM updated
        JOIN users ON updated.user_id = users.id
    """, (post.title, post.content, post.published, id))
    updated_post = Database_Connection.cursor.fetchone()
    Database_Connection.conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return updated_post