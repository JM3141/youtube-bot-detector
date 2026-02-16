import psycopg2

import os

from dotenv import load_dotenv
load_dotenv()


DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT =os.getenv("DB_PORT")


connection_params = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}

def get_connection():
    try: 
       #establishing connection to server
       connection = psycopg2.connect(**connection_params)
       print("Connection established!")
       return connection

    except psycopg2.OperationalError as e:
       print("Connection failed: could not connect to server", e)

    except psycopg2.Error as e:
       print("Database error:", e)









