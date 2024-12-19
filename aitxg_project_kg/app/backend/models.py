#models.py defines the schemas using SQLalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, BLOB
from sqlalchemy.orm import relationship
from .db_setup import Base
from sqlalchemy.sql import func #for time_created

class User(Base):
    __tablename__ = "users"

    #autoincrement replaces SERIAL
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    time_created = Column(TIMESTAMP, default=func.current_timestamp)

    #relationship indicates "Recipe" class is child of "user" 
    #cascade means that all child recipes of a user will be deleted when that user is deleted
    recipes = relationship("Recipe", back_populates="user", cascade="all, delete-orphan")
    #cascade... this picks one database if there are still multiple databases

class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    recipe_name = Column(Text, unique=True)
    specifications_text = Column(Text)
    recipe_output = Column(Text)
    file_url = Column(String, nullable=False) #It is better practice to store the image's url rather than its byte encoding 
    time_saved = Column(TIMESTAMP, default=func.current_timestamp())

    #a recipe belongs to one user
    user = relationship("User", back_populates="recipes")

    recipe_additional_texts = relationship("RecipeAdditionalText", back_populates="recipe", cascade="all, delete-orphan")

#A recipe can have an unlimited number of additional prompts to the model and responses
#from the model. Each prompt-response pair is stored in this database
class RecipeAdditionalText(Base):
    __tablename__ = "recipe_additional_texts"

    recipe_add_text_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    time_saved = Column(TIMESTAMP, default=func.current_timestamp())

    #A recipe text belongs to one recipe
    recipe = relationship("Recipe", back_populates="recipe_additional_texts")