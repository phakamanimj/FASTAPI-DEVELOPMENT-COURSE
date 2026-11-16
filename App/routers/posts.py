from fastapi import FastAPI, HTTPException, Response, status ,Depends ,APIRouter 
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import time

from App import Auth2
from ..import Model,Schemas,Database_Connection

router = APIRouter()


@router.get("/posts",status_code=status.HTTP_200_OK) #decorator
def get_posts():
    Database_Connection.cursor.execute("SELECT * FROM posts") #execute the SQL statement to get all posts from the database
    post = Database_Connection.cursor.fetchall()
    return post

@router.get("/getmy_posts",status_code=status.HTTP_200_OK)
def getmy_posts(current_user: Schemas.TokenData = Depends(Auth2.get_current_user)):
  Database_Connection.cursor.execute("SELECT * FROM posts WHERE user_id = %s", (int(current_user.id),))
  posts = Database_Connection.cursor.fetchall()
  return posts


@router.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int,post: Schemas.Post):
    Database_Connection.cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = Database_Connection.cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post 
@router.get("/getpost/{id}",status_code=status.HTTP_200_OK)
def get_my_post(id :int,current_user: Schemas.TokenData=Depends(Auth2.get_current_user)):
    Database_Connection.cursor.execute("SELECT * FROM posts WHERE id = %s",(id,))
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

@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Schemas.Post,get_current_user: int = Depends(Auth2.get_current_user)):
    new_post = Model.Post(user_id=get_current_user.id, **new_post.dict())#checking if the user is logged in or not and then getting the user id from the token and then creating a new post with the user id
    Database_Connection.cursor.execute("INSERT INTO posts (title,content,published,user_id) VALUES (%s, %s, %s, %s) RETURNING *",(new_post.title, new_post.content, new_post.published, new_post.user_id))
    new_post = Database_Connection.cursor.fetchone()
    Database_Connection.conn.commit()
    return  new_post

@router.put("/posts/{id}")
def update_post(id: int, post: Schemas.Post,get_current_user: int = Depends(Auth2.get_current_user)):
    updated_post = Model.Post(user_id=get_current_user.id, **post.dict())
    Database_Connection.cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    updated_post = Database_Connection.cursor.fetchone()
    Database_Connection.conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": updated_post}



