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
from .routers import posts,Users,Authication


app = FastAPI()



#@app.get("/sqlalchemy", status_code=status.HTTP_200_OK)
##def test_posts(db: Session = Depends(database.get_db())):
 #   posts = db.query(Model.Post).all() #this will get all the posts from our database using SQLAlchemy
 #   return {"data": posts}

app.include_router(posts.router)
app.include_router(Users.router)
app.include_router(Authication.router)


