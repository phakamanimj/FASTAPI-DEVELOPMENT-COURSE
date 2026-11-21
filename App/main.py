from fastapi import FastAPI,Depends 
from .import Model
from .database import engine
from .routers import posts,Users,Authication


app = FastAPI()

Model.Base.metadata.create_all(bind=engine)

#@app.get("/sqlalchemy", status_code=status.HTTP_200_OK)
##def test_posts(db: Session = Depends(database.get_db())):
 #   posts = db.query(Model.Post).all() #this will get all the posts from our database using SQLAlchemy
 #   return {"data": posts}

app.include_router(posts.router)
app.include_router(Users.router)
app.include_router(Authication.router)


