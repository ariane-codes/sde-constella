import tkinter as tk
import tkinter.font as tkFont
from database.database import Database


class Login(tk.Frame):
    def __init__(self, parent, db, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.db = db
        self.controller = controller
        self.show_error_message = False
        self.error_message = ""

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        font = tkFont.Font(family="Helvetica", size=24, weight="bold")

        # Initialize rest of the GUI here.
        title = tk.Label(self, text="Welcome to Constella!")
        title.grid(row=0, column=0, columnspan=4)
        title.configure(font=font)

        username = tk.StringVar()
        password = tk.StringVar()

        # Username Label
        usernameLabel = tk.Label(self, text="Username")
        usernameLabel.grid(row=1, column=1)

        # Username write box
        userEntry = tk.Entry(self, textvariable=username)
        userEntry.grid(row=1, column=2)

        # Password Label
        passwordLabel = tk.Label(self, text="Password")
        passwordLabel.grid(row=3, column=1)

        # Password write box
        passwordEntry = tk.Entry(self, textvariable=password, show="*")
        passwordEntry.grid(row=3, column=2)
        title.configure(bg="light grey")

        loginButton = tk.Button(self, text="Login", command=lambda: self.handle_login(username, password))
        loginButton.grid(row=4, column=0, columnspan=4)

    def handle_login(self, email, password):
        response = self.db.login(email.get(), password.get())
        if response["status"] == 200:
            self.controller.show_frame("ReviewList")
        else:
            self.show_error_message = True
            self.error_message = "Error logging in"



