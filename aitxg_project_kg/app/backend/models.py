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
    recipe_text = Column(Text)
    ingredients_text = Column(Text)
    image = Column(BLOB)
    time_saved = Column(TIMESTAMP, default=func.current_timestamp())

    #relationship indicates "User" class is parent of "recipes"
    #1 user cannot have replica recipes
    user = relationship("User", back_populates="recipes")


