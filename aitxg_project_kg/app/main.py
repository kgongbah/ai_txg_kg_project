from fastapi import FastAPI
from app.backend.db_setup import engine, database
from app.backend.models import Base
from .middleware import CustomMiddleware

#Initialize the database
print("Initializing the database...")
try:    
    Base.metadata.create_all(bind=engine)
    print("Database initalized successfully.")
except Exception as e:
    print(f"Error creating database: {e}")

#Initialize FastAPI app
app = FastAPI()

#Add your custom middleware
app.add_middleware(CustomMiddleware)

#Sample route
@app.get("/")
async def root():
    return {"message": "Hi world :)"}


