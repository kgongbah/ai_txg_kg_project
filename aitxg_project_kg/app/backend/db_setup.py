#db_setup defines connection and setup of databases
from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Defines the connection to a SQLite database in file text.db.
#Later, we can replace this with a PostgreSQL URL
DATABASE_URL = "sqlite:///./test.db"

#Connection to database
database = Database(DATABASE_URL) 

#SQLAlchemy engine, the engine allows us to write and execute SQL queries
#in our python script
engine = create_engine(DATABASE_URL) 

#Base class for declarative models. The base class is used to
#define our models (tables). MetaData object holds schema info
Base = declarative_base(metadata=MetaData()) 

#Session for interacting with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Retrieve dependency for daabase sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()