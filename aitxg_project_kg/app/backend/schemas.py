#schemas.py ensures inputs and outputs conform to structures/types
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    time_created: datetime

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    #user_id: int
    username: str
    email: EmailStr
    password: str
    time_created: datetime
    #recipes: List["RecipeResponse"] = []

    class Config:
        orm_mode = True
        from_attributes = True