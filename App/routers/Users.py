from fastapi import FastAPI, HTTPException, Response, status ,Depends,APIRouter
import bcrypt
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


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))



@router.get("/users",status_code=status.HTTP_200_OK,) #decorator
def get_users():
    cursor.execute("SELECT * FROM users") #execute the SQL statement to get all users from the database
    user = cursor.fetchall()
    return user

@router.post("/create_user", status_code=status.HTTP_201_CREATED,response_model=Schemas.UserOut)
def create_user(new_user: Schemas.User):
    #before we create a user we need to hash a password
    hashed_password = hash_password(new_user.password)
    new_user.password = hashed_password
    cursor.execute("INSERT INTO users (name,email,password) VALUES (%s, %s, %s) RETURNING *",(new_user.name, new_user.email, new_user.password))
    new_user = cursor.fetchone()
    conn.commit()
    return  new_user