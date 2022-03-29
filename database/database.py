import mysql.connector as mysql
import os
from dotenv import load_dotenv

class Database:
    # The database class takes the database name as a parameter to enable switching
    # between dev and stg
    def __init__(self, database):
        self.db = database
        
    # private database connection function
    def __connect(self):
        try:
            # load environment variables from .env file
            load_dotenv()
            self.mydb = mysql.connect(
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                db = self.db
            )
            print("Database connected")
        except mysql.Error as e:
            print(e)
        self.mycursor = self.mydb.cursor()

    # private database connection close function
    def __close(self):
        try:
            self.mycursor.close()
            self.mydb.close()
            print("Database connection closed")
        except mysql.Error as e:
            print(e)

    # database query funtion takes sql query as a string and prints + returns results
    def query(self, sql):
        self.__connect()
        try:
            self.mycursor.execute(sql)
            myresult = self.mycursor.fetchall()
            self.__close()
            return myresult
        except mysql.Error as e:
            print(e) 
            self.__close()

    # database login funcion takes username and password as parameters
    # and returns dictionary containing status & message
    def login(self, username, password):
        # check db for username
        sql = "select * from employee where username = %s"
        val = username
        self.__connect()
        try:
            self.mycursor.execute(sql, (val,))
        except mysql.Error as e:
            print(e)
        myresult = self.mycursor.fetchone()
        self.__close()
        # if username is found check password
        if myresult:
            # if passed password parameter matches password for matched username result(column 5) return 200 - success
            if password == myresult[5]:
                return {"status": 200, "message": "Login successful"}
            # if password doesn't match return 400 - Error 
            else:
                return {"status": 400, "message": "Incorrect username or password"}
        # if username is not found return 400 - Error 
        else:
            return {"status": 400, "message": "Incorrect username or password"}
        


