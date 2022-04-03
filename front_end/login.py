import tkinter as tk
from database.database import Database


class Login(tk.Frame):
    def __init__(self, parent, db, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.db = db
        self.controller = controller

        # Initialize rest of the GUI here.
        title = tk.Label(self, text="Welcome to Constella!")
        title.place(x=320, y=30)
        title.config(font=("Verdana", 24))
        title.configure(bg="light grey")

        username = tk.StringVar()
        password = tk.StringVar()

        # Username Label
        usernameLabel = tk.Label(self, text="Username")
        usernameLabel.place(x=320, y=200)
        usernameLabel.configure(bg="light grey")

        # Username write box
        userEntry = tk.Entry(self, textvariable=username)
        userEntry.place(x=397, y=197)

        # Password Label
        passwordLabel = tk.Label(self, text="Password")
        passwordLabel.place(x=320, y=250)
        passwordLabel.configure(bg="light grey")

        # Password write box
        passwordEntry = tk.Entry(self, textvariable=password, show="*")
        passwordEntry.place(x=397, y=250)
        title.configure(bg="light grey")

        # login button to enter to Constella
        # Paola: The command here will be something like
        # command=lambda: self.db.login(username, password)
        # You'll have to experiment or wrap that function in another one
        # So that you can handle the messages.

        # Right now, the button just switches to the review list.

        loginButton = tk.Button(self, text="Login", command=lambda: controller.show_frame("ReviewList"))
        loginButton.place(x=450, y=340)




