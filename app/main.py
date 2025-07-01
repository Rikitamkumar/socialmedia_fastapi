from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from app import models
from .database import engine

from app.routers import post, user, auth,likes


models.Base.metadata.create_all(bind=engine)  # It tells SQLAlchemy: Create all the tables in the database that are defined in the models — if they don’t already exist.

origins = ['*']

app = FastAPI()


#CORS (Cross-Origin Resource Sharing) implementation

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# while True: # this code does establish a connection to a PostgreSQL database using the psycopg2 library.
#     try:
#         conn = psycopg2.connect(host='localhost', database='socialmedia_fastapi', user= 'postgres', password ='rikitam123', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successdull")
#         break
#     except Exception as e:
#         print("Connection Failed due to: ",e)
#         time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)

@app.get("/")
async def root():
    
    return {"message": "This is a root page"}

