from fastapi import FastAPI, HTTPException, Response, status ,Depends,APIRouter
from ..import Model,Schemas,Database_Connection,utils


router = APIRouter()


@router.get("/users",status_code=status.HTTP_200_OK,) #decorator
def get_users():
    Database_Connection.cursor.execute("SELECT * FROM users") #execute the SQL statement to get all users from the database
    user = Database_Connection.cursor.fetchall()
    return user

@router.post("/create_user", status_code=status.HTTP_201_CREATED,response_model=Schemas.UserOut)
def create_user(new_user: Schemas.User):
    #before we create a user we need to hash a password
    hashed_password = utils.hash_password(new_user.password)
    new_user.password = hashed_password
    Database_Connection.cursor.execute("INSERT INTO users (name,email,password) VALUES (%s, %s, %s) RETURNING *",(new_user.name, new_user.email, new_user.password))
    new_user = Database_Connection.cursor.fetchone()
    Database_Connection.conn.commit()
    return  new_user