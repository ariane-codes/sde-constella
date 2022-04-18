import pytest
import os
import mysql.connector as mysql
from dotenv import load_dotenv

@pytest.fixture
def db_connect():
    try:
        # load environment variables from .env file
        load_dotenv()
        mydb = mysql.connect(
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            db = os.getenv('DB_DATABASE')
        )
        print("PYTEST: Database connected")
    except mysql.Error as err:
        print(err)
    return mydb


