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

@pytest.fixture
def db_close(mycursor, mydb):
    try:
        mycursor.close()
        mydb.close()
        print("PYTEST: Database connection closed")
    except mysql.Error as err:
        print(err)

@pytest.fixture
def query(sql, vals=None, fetchone=False):
    """  sql query function that takes an sql query as a string, a tuple of variables
    and the option to query for one or many, default is many
    returns and prints results """
    mydb = db_connect()
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql, vals)
        if fetchone:
            myresult = mycursor.fetchone()
        else:
            myresult = mycursor.fetchall()
        db_close(mycursor, mydb)
        return myresult
    except mysql.Error as err:
        print(err)
        db_close(mycursor, mydb)
        return err

