from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="Maboni123#",
    host="localhost",
    port=5432,
    database="Fast API Database",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():# this function allows us to get a session to our database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


