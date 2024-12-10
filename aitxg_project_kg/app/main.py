from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db_setup import engine, database, get_db
from backend.models import Base, User
from backend.crud_user import (
    get_user_by_id, 
    get_user_by_email,
    get_all_users, 
    create_user, 
    update_user_by_id, 
    delete_user_by_id)
from middleware import CustomMiddleware
from backend.schemas import UserCreate, UserResponse
from datetime import datetime

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

#Define the root path
@app.get("/")
async def read_root():
    return {"message": "Welcome to Kenny's AITXG project."}

#Create new user
@app.post("/users/", response_model=UserResponse)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already registered.")
    new_user = create_user(db, user.username, user.email, user.password, datetime.now())
    print(new_user)
    return UserResponse.from_orm(new_user)

#Read existing user by user_id
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_existing_user(user_id: int, db: Session = Depends(get_db)):
    user_to_read = get_user_by_id(db, user_id) 
    if not user_to_read:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserResponse.model_validate(user_to_read)

#http://localhost:80/docs

