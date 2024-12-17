from sqlalchemy.orm import Session
from ..models import Recipe
from datetime import datetime

#Create a new recipe
def create_new_recipe(db: Session, user_id: int, recipe_name: str, specifications_text: str, recipe_output: str, file_url: str, time_saved: datetime):
    recipe = Recipe(
        user_id = user_id, 
        recipe_name = recipe_name, 
        specifications_text = specifications_text, 
        recipe_output = recipe_output,
        file_url = file_url,
        time_saved = time_saved)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    print("Here2")
    return recipe

#Read recipe by recipe_id
def read_recipe_by_recipe_id(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

#Read all recipes by user_id
def read_all_recipes_by_user_id(db: Session, user_id: int):
    return db.query(Recipe).filter(Recipe.user_id == user_id).all()

#Read recipe by user_id and recipe name
def read_recipe_by_user_id_and_recipe_name(db: Session, user_id: int, recipe_name: str):
    return db.query(Recipe).filter(Recipe.user_id == user_id, Recipe.recipe_name == recipe_name).first()
    #Note that using python "and" within .filter() is NOT OK!

#Update recipe by recipe_id
#This function can only update recipe_name. We cannot update the image or specifications_text.
#To update recipe_text, see function in crud_recipe_text
def update_recipe_name_by_recipe_id(db: Session, recipe_id: int, recipe_name: str = None):
    recipe_to_update = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if recipe_to_update:
        if recipe_name: recipe_to_update.recipe_name = recipe_name
    db.commit()
    db.refresh(recipe_to_update)
    return recipe_to_update

#Delete recipe by recipe_id
def delete_recipe_by_recipe_id(db: Session, recipe_id: int):
    recipe_to_delete = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if recipe_to_delete:
        db.delete(recipe_to_delete)
        db.commit()
    return recipe_to_delete