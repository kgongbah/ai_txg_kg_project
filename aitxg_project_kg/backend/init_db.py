from db_setup import engine
from models import Base

print("Initializing the database...")

try:    
    Base.metadata.create_all(bind=engine)
    print("Database initalized successfully.")
except Exception as e:
    print(f"Error creating database: {e}")