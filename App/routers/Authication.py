from fastapi import FastAPI, HTTPException, Response, status ,Depends,APIRouter
from ..import Model,Schemas,Database_Connection,utils,Auth2

router = APIRouter(tags=["Authication"])

@router.post("/login")
def login(user_credentials: Schemas.Userlogin):
    Database_Connection.cursor.execute("SELECT * FROM users WHERE email = %s",(user_credentials.email,),)
    user = Database_Connection.cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials",)

    if not utils.verify_password(user_credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials",)
    
    token = Auth2.create_access_token(data={"user_id": user["id"]})
    return {"Token": token}