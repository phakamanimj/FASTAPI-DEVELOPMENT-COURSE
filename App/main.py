from fastapi import FastAPI, HTTPException, Response, status ,Depends
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .import Model,Schemas
from .database import engine ,SessionLocal
from sqlalchemy.orm import Session



Model.Base.metadata.create_all(bind=engine) #this will create the tables in our database if they do not exist already

app = FastAPI()


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


#@app.get("/sqlalchemy", status_code=status.HTTP_200_OK)
##def test_posts(db: Session = Depends(database.get_db())):
 #   posts = db.query(Model.Post).all() #this will get all the posts from our database using SQLAlchemy
 #   return {"data": posts}


@app.get("/posts",status_code=status.HTTP_200_OK) #decorator
def get_posts():
    cursor.execute("SELECT * FROM posts") #execute the SQL statement to get all posts from the database
    post = cursor.fetchall()
    return post


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int,post: Schemas.Post):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post 


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return  deleted_post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Schemas.Post):
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *",(new_post.title, new_post.content, new_post.published,))
    new_post = cursor.fetchone()
    conn.commit()
    return  new_post

@app.put("/posts/{id}")
def update_post(id: int, post: Schemas.Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": updated_post}

@app.get("/users",status_code=status.HTTP_200_OK) #decorator
def get_users():
    cursor.execute("SELECT * FROM users") #execute the SQL statement to get all users from the database
    user = cursor.fetchall()
    return user

@app.post("/create_user", status_code=status.HTTP_201_CREATED,response_model=Schemas.UserOut)
def create_user(new_user: Schemas.User):
    cursor.execute("INSERT INTO users (name,email,password) VALUES (%s, %s, %s) RETURNING *",(new_user.name, new_user.email, new_user.password))
    new_user = cursor.fetchone()
    conn.commit()
    return  new_user
