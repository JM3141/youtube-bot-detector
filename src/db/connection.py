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

connection = psycopg2.connect(**connection_params)

cursor = connection.cursor()

print("Connection established!")

cursor.close()
connection.close()



