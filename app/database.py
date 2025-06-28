from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}'

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"    #connecting to  a sqllite database
# SQLALCHEMY_DATABASE_URL[= "postgresql://user:password@postgresserver/db"   #postgres syntax

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#Dependency -  Dependency Injection -- external resources or services (like a database session, auth logic, or config) are automatically provided (injected) to parts of code.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
