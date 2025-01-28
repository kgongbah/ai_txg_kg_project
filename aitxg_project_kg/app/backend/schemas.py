#schemas.py ensures inputs and outputs conform to structures/types
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime
from fastapi import UploadFile

##########################################################################################
# USER PYDNATIC MODELS
##########################################################################################

class UserBase(BaseModel):
    username: str
    email: EmailStr
    #time_created: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    user_id: int
    username: str
    email: EmailStr
    password: str
    time_created: datetime
    recipes: List["RecipeResponse"] = []

    class Config:
        orm_mode = True
        from_attributes = True

##########################################################################################
# RECIPE PYDANTIC MODELS
##########################################################################################

class RecipeBase(BaseModel):
    recipe_name: str
    specifications_text: Optional[str] = None
    recipe_output: str
    time_saved: datetime

class RecipeCreate(RecipeBase):
    recipe_name: str
    specifications_text: Optional[str] = None
    recipe_output: str
    #image: UploadFile
    #Don't include image, let FastAPI File and FileUpload handle it

class RecipeUpdate(RecipeBase):
    recipe_name: Optional[str] = None
    recipe_output: Optional[str] = None

class RecipeResponse(RecipeBase):
    recipe_id: int
    user_id: int
    recipe_name: str
    specifications_text: str
    recipe_output: str
    file_url: str
    time_saved: datetime

    class Config:
        orm_mode = True
        from_attributes = True

##########################################################################################
# RECIPE ADDITIONAL TEXT PYDANTIC MODELS
##########################################################################################

class RecipeAddTextBase(BaseModel):
    # user_id: int
    # recipe_id: int
    prompt: str
    response: str
    # time_saved: datetime

class RecipeAddTextCreate(RecipeAddTextBase):
    prompt: str


class RecipeAddTextUpdate(RecipeAddTextBase):
    #prompt: str
    response: str

class RecipeAddTextResponse(RecipeAddTextBase):
    recipe_add_text_id: int
    user_id: int
    recipe_id: int
    prompt: str
    response: str
    time_saved: datetime

    class Config:
        orm_mode = True
        from_attributes = True