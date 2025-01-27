from sqlalchemy.orm import Session
from ..models import User
from datetime import datetime

#Create new user
def create_user(db: Session, username: str, email: str, password: str, time_created: datetime):
    user = User(username = username, email = email, password = password, time_created = time_created)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 

#Verify password when user tries to login
def verify_password(db: Session, username: str, inputted_password: str):
    user = get_user_by_username(db, username)
    user_password = user.password
    return user_password == inputted_password

#Read user by user_id
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first() #is first necessary

#Read user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

#Read user by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

#Read all users
def get_all_users(db: Session):
    return db.query(User).all()

#Update user by user_id
def update_user_by_id(db: Session, user_id: int, username: str = None, email: str = None, password: str = None):
    user = db.query(User).filter(User.user_id == user_id).first() #Get user by user_id
    if user: #check if user exists
        if username: user.username = username 
        if email: user.email = email
        if password: user.password = password
    db.commit()
    db.refresh(user)
    return user

#Delete user by user_id
def delete_user_by_id(db: Session, user_id: int):
    user_to_delete = db.query(User).filter(User.user_id == user_id).first()
    if user_to_delete: 
        db.delete(user_to_delete)
        db.commit()
    return user_to_delete




    