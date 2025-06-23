from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:rikitam123@localhost/socialmedia_fastapi'

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"    #connecting to  a sqllite database
# SQLALCHEMY_DATABASE_URL[= "postgresql://user:password@postgresserver/db"   #postgres syntax

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
