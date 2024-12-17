from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form, staticfiles
from sqlalchemy.orm import Session
from backend.db_setup import engine, database, get_db
from backend.models import Base, User
import backend.crud.crud_user as crud_user
import backend.crud.crud_recipe as crud_recipe
from middleware import CustomMiddleware
from backend.schemas import UserCreate, UserResponse, UserUpdate, RecipeCreate, RecipeResponse, RecipeUpdate
from datetime import datetime
from typing import Optional
import io
from uuid import uuid4

#Initialize the database
print("Initializing the database...")
try:    
    Base.metadata.create_all(bind=engine)
    print("Database initalized successfully.")
except Exception as e:
    print(f"Error creating database: {e}")

#Initialize FastAPI app
app = FastAPI()

# Serve the /static directory
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")

#Add your custom middleware
app.add_middleware(CustomMiddleware)

#Define the root path
@app.get("/")
async def read_root():
    return {"message": "Welcome to Kenny's AITXG project."}

##########################################################################################
# USER API ROUTES
##########################################################################################

#Create new user
@app.post("/users/", response_model=UserResponse)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user_email = crud_user.get_user_by_email(db, user.email)
    existing_user_username = crud_user.get_user_by_username(db, user.username)
    if existing_user_email:
        raise HTTPException(status_code=400, detail="User with this email already registered.")
    elif existing_user_username:
        raise HTTPException(status_code=400, detail="User with this username already registered.")
    new_user = crud_user.create_user(db, user.username, user.email, user.password, datetime.now())
    print(f"New user created: user_id: {new_user.user_id}, username: {new_user.username}, email: {new_user.email}")
    return UserResponse.from_orm(new_user)

#Read existing user by user_id
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_existing_user(user_id: int, db: Session = Depends(get_db)):
    user_to_read = crud_user.get_user_by_id(db, user_id) 
    if not user_to_read:
        raise HTTPException(status_code=404, detail="User to read not found.")
    print(f"Read user: user_id: {user_to_read.user_id}, username: {user_to_read.username}, email: {user_to_read.email}")
    return UserResponse.from_orm(user_to_read)

#Update existing user by user_id
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_existing_user(user_update: UserUpdate, user_id: int, db: Session = Depends(get_db)):
    #Check if the user exists
    user_to_update = crud_user.get_user_by_id(db, user_id)
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User to update not found.")
    
    #Update the user with new details
    updated_user = crud_user.update_user_by_id(
        db, 
        user_id, 
        username=user_update.username, 
        email=user_update.email,
        password=user_update.password)
    
    #Check if user was updated successfully.
    if not updated_user:
        raise HTTPException(status_code=400, detail="Unable to update user.")
    print(f"User with user_id {user_id} updated - username: {updated_user.username} - email: {updated_user.email} - password: {updated_user.email}")
    return UserResponse.from_orm(updated_user)

#Delete existing user by user_id
@app.delete("/users/{user_id}", response_model=UserResponse)
async def delete_existing_user(user_id: int, db: Session = Depends(get_db)):

    #Check if the user to delete exists.
    user_to_delete = crud_user.delete_user_by_id(db, user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User to delete not found.")
    
    print(f"User with user_id {user_id} deleted - username: {user_to_delete.username} - email: {user_to_delete.email} - password: {user_to_delete.password}")
    return UserResponse.from_orm(user_to_delete)

##########################################################################################
# RECIPE API ROUTES
##########################################################################################
    
#Create a recipe by user_id
@app.post("/user/{user_id}/recipes/", response_model=RecipeResponse)
async def create_new_recipe_by_user_id(
    user_id: int,
    recipe_name: str = Form(...),
    specifications_text: Optional[str] = Form(None),
    #recipe_output: str = Form(...),
    #time_saved: datetime = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    #Check if the user exists
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Recipe's parent user does not exist.")
    
    #Check if the recipe's name has already been used by the user
    recipe_name_exists = crud_recipe.read_recipe_by_user_id_and_recipe_name(db, user_id, recipe_name)
    if recipe_name_exists:
        raise HTTPException(status_code=404, detail=f"User has already created a recipe with this name: {recipe_name}")
    
    #Temporary definition for recipe_output. Eventually this will be AWS Sagemaker generated text
    recipe_output = f"recipe_output for {recipe_name}."

    #Generate a unique filename
    unique_file_name = f"{uuid4()}_{file.filename}"

    #Specify the path where the file will be saved, used internally by CRUD
    file_path = f"static/uploads/{unique_file_name}"

    #Specify the file url, used by clients (front-end, APIs)
    file_url = f"static/uploads/{unique_file_name}"

    #Read the file contents and then save to server's file storage
    with open(file_path, "wb") as buffer: 
        buffer.write(await file.read())
    
    new_recipe = crud_recipe.create_new_recipe(
        db = db,
        user_id=user_id,
        recipe_name=recipe_name,
        specifications_text=specifications_text,
        recipe_output=recipe_output,
        file_url=file_url,
        time_saved=datetime.now()
        )
    
    if not new_recipe:
        raise HTTPException(status_code=500, detail="Error creating new recipe.")
    else: 
        print(f"User with user_id {new_recipe.user_id} created recipe - recipe name: {new_recipe.recipe_name} - recipe id: {new_recipe.recipe_id}")
        return RecipeResponse.from_orm(new_recipe)



"""
Demo steps:
1. Delete test.db and launch app: uvicorn main:app --host 0.0.0.0 --port 80
2. Go to http://localhost:80/docs
3. Add a new user
4. Try adding a new user with the same username -> look at error message
5. Try adding a new user with the same email -> look at error message
6. Add a second user with a unique username and email
7. Kill the app (CTRL+C) and follow commands:
    1. sqlite3
    2. .open test.db
    3. select * from users;
8. You should be able to see your new users
9. .exit and run app again: uvicorn main:app --host 0.0.0.0 --port 80
10. Try to update user where user_id = 1, change username, set email and password to null
11. Try to delete user where user_id = 1
"""


