import mysql.connector as mysql

class Database:
    def __init__(self, database):
        self.db = database

    # private database connection function
    def __connect(self):
        try:
            self.mydb = mysql.connect(
                host = '51.158.57.154',
                port = '10151',
                user = 'constella_developer_jk7T',
                password = 'gAaqjinVH9R+bsjqr8nG',
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
            for x in myresult:
                print(x[4])
            return myresult
        except mysql.Error as e:
            print(e)        
        self.__close()

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
        # if username is found check password
        if myresult:
            # if passed password parameter matches password for matched user result(column 5) return 200 - success
            if password == myresult[5]:
                return {"status": 200, "message": "Login successful"}
            # if password doesn't match return 400 - Error 
            else:
                return {"status": 400, "message": "Incorrect username or password"}
        # if username is not found return 400 - Error 
        else:
            return {"status": 400, "message": "Incorrect username or password"}
        self.__close()


