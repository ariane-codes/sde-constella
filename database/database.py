import mysql.connector as mysql
import os
from dotenv import load_dotenv

class Database:
    # Private database connection function
    def __connect(self):
        try:
            # load environment variables from .env file
            load_dotenv()
            self.mydb = mysql.connect(
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                db = os.getenv('DB_DATABASE')
            )
            print("Database connected")
        except mysql.Error as e:
            print(e)
        self.mycursor = self.mydb.cursor()

    # Private database connection close function
    def __close(self):
        try:
            self.mycursor.close()
            self.mydb.close()
            print("Database connection closed")
        except mysql.Error as e:
            print(e)


    # Database login funcion takes username and password as parameters
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
        

    # Database query funtion takes sql query as a string and prints + returns results
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

    # This function returns 'page_size' number of reviews that have not been 
    # assigned to an employee, have 'stars' number of stars or less and have 
    # and id number greater than 'last_review_id' ordered by created date decending
    #
    def get_reviews(self, stars=3,page_size=5, last_review_id=0):
        self.__connect()
        sql = "SELECT * FROM review WHERE employee_id IS NULL AND star_rating"\
        " <= %s AND id > %s ORDER BY id DESC LIMIT %s"
        vals = (stars, last_review_id, page_size)
        try:
            self.mycursor.execute(sql, vals)
            # Tested with fetchmany(page_size) but this was slower than using sql LIMIT
            myresult = self.mycursor.fetchall()
            self.__close()
            reviews = []
            review = {}
            for index, row in enumerate(myresult):
                temp_dict = {"review_id" : row[0],
                             "review_product_title" : row[1],
                             "review_product_category" : row[2],
                             "review_star_rating" : row[3],
                             "review_status" : row[4],
                             "review_title" : row[5],
                             "review_body" : row[6],
                             "review_purchase_price" : row[7],
                             "review_created" : row[8],
                             "review_customer_id" : row[9],
                             "review_employee_id" : row[10]
                            }
                reviews.append(temp_dict)
            return reviews
        except mysql.Error as e:
            print(e) 
            self.__close()
