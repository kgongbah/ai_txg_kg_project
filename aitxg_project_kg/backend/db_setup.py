import psycopg2
from psycopg2 import sql

print("Starting the database setup script...")

#configure the database's parameters using dictionary. We must connect to the
#default database "postgres" before we can begin executing commands like
#CREATE DATABASE
db_params = {
    'dbname': 'postgres',  # Connect to the default 'postgres' database
    'user': '642672',
    'password': 'kg_password',
    'host': 'localhost', #use local host while on your local machine
    'port': '5432' #default port for PostgreSQL to listen for connections
}

#Connect to PostgreSQL
try:
    my_connection = psycopg2.connect(**db_params) 
    #** "unpacks", allows dictionary to be passed into .connect()
    my_connection.autocommit = True 
    #if you don't autocommit or .commit(), any changes executed to the database aren't saved
    cursor = my_connection.cursor() #cursor class allows python to run SQL
    cursor.execute("CREATE DATABASE kg_database;")
    print("Database successfully created.")

except Exception as e: #throw error if unable to create database
    print(f"Error creating default database: {e}")

finally:
    cursor.close()
    my_connection.close()

#Create the new database, kg_database

db_params['dbname'] = 'kg_database'

#Connect to new database
try: 
    my_connection = psycopg2.connect(**db_params)
    my_connection.autocommit = True
    cursor = my_connection.cursor()

    #Create the tables
    cursor.execute("""
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY, --SERIAL indicates unique id upon row creation
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP --default sets timestamp to current_timestamp unless otherwise specified           
        );
                   
        CREATE TABLE recipes (
            recipe_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id),
            image BLOB,
            ingredients TEXT,
            recipe TEXT,
            time_saved TIMESTAMP DEFAULT CURRENT_TIMESTEMP
        );
    """)

    print("Tables created successfully.")

except Exception as e:
    print(f"Error connecting to database or creating table: {e}")

finally:
    cursor.close()
    my_connection.close()










