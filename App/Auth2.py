from datetime import timedelta ,datetime
from jose  import JWTError,jwt
from .import Schemas
from fastapi import  HTTPException, Response, status ,Depends
from fastapi.security import OAuth2PasswordBearer
#SECRETE_KEY = 
#ALGORITHM = "HS256"
#Expiration time in minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    #expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #if expires_delta:
      # expire = datetime.utcnow() + expires_delta
    #else:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str,credintials_exeption): #method thats verify if the token is stll valid or not
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credintials_exeption
        token_data = Schemas.TokenData(id=str(id))
    except JWTError:
        raise credintials_exeption
    return token_data
def get_current_user(token: str = Depends(oauth2_scheme)):
    credintials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credintials_exeption)