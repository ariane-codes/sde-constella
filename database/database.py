import os
import mysql.connector as mysql
from dotenv import load_dotenv


class Database:
    """ Wrapper class for all database related funtions"""
    def __init__(self):
        self.mydb = None
        self.mycursor = None

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
        except mysql.Error as err:
            print(err)
        self.mycursor = self.mydb.cursor()

    # Private database connection close function
    def __close(self):
        try:
            self.mycursor.close()
            self.mydb.close()
            print("Database connection closed")
        except mysql.Error as err:
            print(err)

    def login(self, email, password):
        """  Login function takes a email and password
        and returns dictionary containing 'status: 200 and success message'
        or 'status: 400 & login failed message' & employee Id, first name, last name,
        email & username """
        # check db for email
        sql = "select * from employee where email = %s"
        val = email
        self.__connect()
        try:
            self.mycursor.execute(sql, (val,))
        except mysql.Error as err:
            print(err)
        myresult = self.mycursor.fetchone()
        self.__close()
        # if email is found check password
        if myresult:
            # if passed password parameter matches password for matched email
            # result(column 5) return 200 - success
            if password == myresult[5]:
                return {"status": 200,
                        "message": "Login successful",
                        "employee_data": {
                            "emp_id": myresult[0],
                            "emp_first_name": myresult[1],
                            "emp_last_name": myresult[2],
                            "emp_email": myresult[3],
                            "emp_username": myresult[4]
                            }
                        }
            # if password doesn't match return 400 - Error
            return {"status": 400, "message": "Incorrect email or password"}
        # if email is not found return 400 - Error
        return {"status": 400, "message": "Incorrect email or password"} 

    # Database query funtion takes sql query as a string and prints + returns results
    def query(self, sql):
        """  sql query function that takes an sql query as a string
        and returns = prints the results a list object of results """
        self.__connect()
        try:
            self.mycursor.execute(sql)
            myresult = self.mycursor.fetchall()
            self.__close()
            print(myresult)
            return myresult
        except mysql.Error as err:
            print(err)
            self.__close()
            return err

    def get_reviews(self, stars=3, page_size=5, last_review_id=0):
        """This function returns 'page_size' number of reviews that have not been
        assigned to an employee, have 'stars' number of stars or less and have
        and id number greater than 'last_review_id' ordered by created date decending """
        self.__connect()
        if last_review_id > 0:
            sql = "SELECT r.*, c.premier FROM review r LEFT JOIN customer c "\
                "ON r.customer_id = c.id WHERE r.employee_id IS NULL AND r.star_rating "\
                "<= %s AND r.id < %s ORDER BY r.id DESC LIMIT %s"
            vals = (stars, last_review_id, page_size)
        else:
            sql = "SELECT r.*, c.premier FROM review r LEFT JOIN customer c "\
                "ON r.customer_id = c.id WHERE r.employee_id IS NULL AND r.star_rating "\
                "<= %s ORDER BY r.id DESC LIMIT %s"
            vals = (stars, page_size)
        try:
            self.mycursor.execute(sql, vals)
            # Tested with fetchmany(page_size) but this was slower than using sql LIMIT
            myresult = self.mycursor.fetchall()
            self.__close()
            reviews = []
            for row in myresult:
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
                             "review_employee_id" : row[10],
                             "review_customer_premier": row[11]
                            }
                reviews.append(temp_dict)
            return reviews
        except mysql.Error as err:
            print(err)
            self.__close()
            return err

    def assign_review(self, employee_id, review_id):
        """ Takes an employee id and review id and adds the employee to the
        review with the matching review id  """
        self.__connect()
        try:
            sql = "UPDATE review set employee_id = %s\
                   WHERE id = %s"
            vals = (employee_id, review_id)
            self.mycursor.execute(sql, vals)
            self.mydb.commit()
        except mysql.Error as e:
            print("MYSQL Error: " + str(e))
        self.__close()

