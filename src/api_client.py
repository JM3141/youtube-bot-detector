# importing os module for environment variables
import os

# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values
load_dotenv()

#accessing value and storing it in variable
API_KEY = os.getenv("GOOGLE_API_KEY")
