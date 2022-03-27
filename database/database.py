import mysql.connector as mysql

class Database:
    def __init__(self, database):
        self.db = database

    def __connect__(self):
        try:
            self.mydb = mysql.connect(
                host = '51.158.57.154',
                port = '10151',
                user = 'constella_developer_jk7T',
                password = 'gAaqjinVH9R+bsjqr8nG',
                db = self.db
            )
        except mysql.Error as e:
            print(e)
        self.mycursor = self.mydb.cursor()

    def __close__(self):
        try:
            self.mycursor.close()
            self.mydb.close()
            print("Database connection closed")
        except mysql.Error as e:
            print(e)

    def query(self, sql):
        self.__connect__()
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        for x in myresult:
            print(x)
        self.__close__()


