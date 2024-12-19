from sqlalchemy.orm import Session
from ..models import RecipeAdditionalText
from datetime import datetime

#Create new recipe additional text prompt-response pair by user_id and recipe_id
def create_new_recipe_add_text(db: Session, user_id: int, recipe_id: int, prompt: str, response: str, time_saved=datetime):
    recipe_add_text = RecipeAdditionalText(
        user_id=user_id,
        recipe_id=recipe_id,
        prompt=prompt,
        response=response,
        time_saved=time_saved
    )
    db.add(recipe_add_text)
    db.commit()
    db.refresh(recipe_add_text)
    return recipe_add_text

#Read recipe additional text by user_id, recipe_id, recipe_add_text_id
def read_recipe_add_text(db: Session, recipe_add_text_id: int, user_id: int, recipe_id: int):
    return db.query(RecipeAdditionalText).filter(
        RecipeAdditionalText.recipe_add_text_id == recipe_add_text_id,
        RecipeAdditionalText.user_id == user_id,
        RecipeAdditionalText.recipe_id == recipe_id
        ).first()

#Read all recipe additional texts of a user's single recipe by user_id and recipe_id
def read_all_recipe_add_text(db: Session, user_id: int, recipe_id: int):
    return db.query(RecipeAdditionalText).filter(
        RecipeAdditionalText.user_id == user_id,
        RecipeAdditionalText.recipe_id == recipe_id
        ).all()
    
#Update recipe additional text response by user_id, recipe_id, recipe_add_text_id
def update_recipe_add_text(db: Session, recipe_add_text_id: int, user_id: int, recipe_id: int, response: str = None):
    recipe_add_text_to_update = db.query(RecipeAdditionalText).filter(
        RecipeAdditionalText.recipe_add_text_id == recipe_add_text_id,
        RecipeAdditionalText.user_id == user_id,
        RecipeAdditionalText.recipe_id == recipe_id
    ).first()

    if recipe_add_text_to_update:
        if recipe_add_text_to_update.response: recipe_add_text_to_update.response = response

    db.commit()
    db.refresh(recipe_add_text_to_update)
    return recipe_add_text_to_update

#Delete recipe additional text by user_id, recipe_id, recipe_add_text_id
def delete_recipe_add_text(db: Session, recipe_add_text_id: int, user_id: int, recipe_id: int):
    recipe_add_text_to_delete = db.query(RecipeAdditionalText).filter(
        RecipeAdditionalText.recipe_add_text_id == recipe_add_text_id,
        RecipeAdditionalText.user_id == user_id,
        RecipeAdditionalText.recipe_id == recipe_id
    ).first()
    if recipe_add_text_to_delete:
        db.delete(recipe_add_text_to_delete)
        db.commit()
    return recipe_add_text_to_delete