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


    def query(self, sql, vals=None, fetchone=False):
        """  sql query function that takes an sql query as a string, a tuple of variables
        and the option to query for one or many, default is many
        returns and prints results """
        self.__connect()
        try:
            self.mycursor.execute(sql, vals)
            if fetchone:
                myresult = self.mycursor.fetchone()
            else:
                myresult = self.mycursor.fetchall()
            self.__close()
            return myresult
        except mysql.Error as err:
            print(err)
            self.__close()
            return err

    def get_reviews(self, stars=3, page_size=5, last_review_id=0):
        """This function returns 'page_size' number of reviews that have not been
        assigned to an employee, have 'stars' number of stars or less and have
        and id number greater than 'last_review_id' ordered by created date decending """
        if last_review_id > 0:
            sql = "SELECT r.*, c.premier FROM review r LEFT JOIN customer c \
                ON r.customer_id = c.id WHERE r.employee_id IS NULL AND r.star_rating \
                <= %s AND r.id < %s ORDER BY r.id DESC LIMIT %s"
            vals = (stars, last_review_id, page_size)
        else:
            sql = "SELECT r.*, c.premier FROM review r LEFT JOIN customer c \
                ON r.customer_id = c.id WHERE r.employee_id IS NULL AND r.star_rating \
                <= %s ORDER BY r.id DESC LIMIT %s"
            vals = (stars, page_size)
        try:
            myresult = self.query(sql, vals)
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
            return err

    def assign_review(self, employee_id, review_id):
        """ Takes employee id and review id, adds the employee id to the
        review with the matching review id and returns a dictionary containing
        review and customer dictionaries"""
        self.__connect()
        try:
            sql = "UPDATE review set employee_id = %s\
                   WHERE id = %s"
            vals = (employee_id, review_id)
            self.mycursor.execute(sql, vals)
            self.mydb.commit()
            self.__close()
            sql = "SELECT * FROM review\
                   WHERE id = %s"
            vals = (review_id,)
            review = self.query(sql, vals, True)
            sql = "SELECT * FROM customer\
                   WHERE id = %s "
            vals = (review[9],)
            customer = self.query(sql, vals, True)
            return {
                "review": {
                    "id" : review[0],
                    "product_title" : review[1],
                    "product_category" : review[2],
                    "star_rating" : review[3],
                    "status" : review[4],
                    "title" : review[5],
                    "body" : review[6],
                    "purchase_price" : review[7],
                    "created" : review[8],
                    "customer_id" : review[9],
                    "employee_id" : review[10]
                },
                "customer": {
                    "id": customer[0],
                    "name": customer[1],
                    "email": customer[2],
                    "join_date": customer[3],
                    "premier": customer[4]
                }
            }
        except mysql.Error as err:
            print("MYSQL Error: " + str(err))
            self.__close()
            return err
