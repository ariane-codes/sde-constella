from tkinter import *

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


#Create tkinter GUI
window = Tk()

username=StringVar()
password=StringVar()

# Window size and position
window.title("")
window.geometry("900x700")
window.configure(bg="light grey")
window.resizable(width=False, height=False)

# title for Constella main page
title = Label(window, text="Welcome to Constella")
title.place(x=320, y=30)
title.config(font=("Verdana", 24))
title.configure(bg="light grey")

# Username Label
usernameLabel = Label(window, text="Username")
usernameLabel.place(x=320, y=200)
usernameLabel.configure(bg="light grey")

# Username write box
userEntry = Entry(window, textvariable=username)
userEntry.place(x=397, y=197)

# Password Label
passwordLabel = Label(window, text="Password")
passwordLabel.place(x=320, y=250)
passwordLabel.configure(bg="light grey")

# Password write box
passwordEntry = Entry(window, textvariable=password, show="*")
passwordEntry.place(x=397, y=250)
title.configure(bg="light grey")

# login button to enter to Constella
loginButton = Button(window, text="Login", command=login)
loginButton.place(x=450, y=340)

# Our GUI is complete
window.mainloop()


