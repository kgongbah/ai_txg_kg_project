from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db_setup import engine, database, get_db
from backend.models import Base, User
from backend.crud_user import (
    get_user_by_id, 
    get_user_by_email,
    get_user_by_username,
    get_all_users, 
    create_user, 
    update_user_by_id, 
    delete_user_by_id)
from middleware import CustomMiddleware
from backend.schemas import UserCreate, UserResponse, UserUpdate
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
    existing_user_email = get_user_by_email(db, user.email)
    existing_user_username = get_user_by_username(db, user.username)
    if existing_user_email:
        raise HTTPException(status_code=400, detail="User with this email already registered.")
    elif existing_user_username:
        raise HTTPException(status_code=400, detail="User with this username already registered.")
    new_user = create_user(db, user.username, user.email, user.password, datetime.now())
    print(f"New user created: user_id: {new_user.user_id}, username: {new_user.username}, email: {new_user.email}")
    return UserResponse.from_orm(new_user)

#Read existing user by user_id
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_existing_user(user_id: int, db: Session = Depends(get_db)):
    user_to_read = get_user_by_id(db, user_id) 
    if not user_to_read:
        raise HTTPException(status_code=404, detail="User to read not found.")
    print(f"user_id: {user_to_read.user_id}, username: {user_to_read.username}, email: {user_to_read.email}")
    return UserResponse.from_orm(user_to_read)

#Update existing user by user_id
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_existing_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    #Check if the user exists
    user_to_update = get_user_by_id(db, user_id)
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User to update not found.")
    
    #Update the user with new details
    updated_user = update_user_by_id(
        db, 
        user_id, 
        username=user_update.username, 
        email=user_update.email,
        password=user_update.password)
    
    #Check if user was updated successfully.
    if not updated_user:
        raise HTTPException(status_code=400, detail="Unable to update user.")

    return UserResponse.from_orm(updated_user)

#Delete existing user by user_id
@app.delete("/users/{user_id}", response_model=UserResponse)
async def delete_existing_user(user_id: int, db: Session = Depends(get_db)):

    #Check if the user to delete exists.
    user_to_delete = delete_user_by_id(db, user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User to delete not found.")
    
    return UserResponse.from_orm(user_to_delete)
    

"""
Demo steps:
1. Delete test.db and launch app: uvicorn main:app --host 0.0.0.0 --port 80
2. Go to http://localhost:80/docs
3. Add a new user
4. Kill the app (CTRL+C) and follow commands:
    1. sqlite3
    2. .open test.db
    3. select * from users;
5. You should be able to see your new user
6. .exit and run app again: uvicorn main:app --host 0.0.0.0 --port 80
7. Try the same process with a new user with the same username
8. Try the same process with a new user with a different username
7. Try to update user where user_id = 1
8. Try to delete user where user_id = 1
"""


