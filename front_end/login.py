import tkinter as tk
import tkinter.font as tk_font
from database.database import Database


class Login(tk.Frame):
    def __init__(self, parent, db, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.db = db
        self.controller = controller
        # Adding these vars to the constructor, so they're accessible to the other Class methods
        self.email = tk.StringVar()
        self.password = tk.StringVar()

        # Setting column configure so everything is well spread horizontally
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # Title
        font = tk_font.Font(family="Helvetica", size=24, weight="bold")
        title = tk.Label(self, text="Welcome to Constella!")
        title.grid(row=0, column=0, columnspan=4, padx=15, pady=45)
        title.configure(font=font)

        # Email Label
        email_label = tk.Label(self, text="Email")
        email_label.grid(row=1, column=1, sticky=tk.E, padx=15, pady=15)

        # Email write box
        email_entry = tk.Entry(self, textvariable=self.email, width=30)
        email_entry.grid(row=1, column=2, sticky=tk.W, padx=15, pady=15)

        # Password Label
        password_label = tk.Label(self, text="Password")
        password_label.grid(row=3, column=1, sticky=tk.E, padx=15, pady=15)

        # Password write box
        password_entry = tk.Entry(self, textvariable=self.password, show="*", width=30)
        password_entry.grid(row=3, column=2, sticky=tk.W, padx=15, pady=15)

        # Add trace callbacks to the string vars
        self.email.trace("w", self.on_input_change)
        self.password.trace("w", self.on_input_change)

        # The login button is also added to the constructor (self.)
        # so we can access it through other methods
        self.login_button = tk.Button(self, text="Login",
                                      # Calling handle_login as the command for the login button.
                                      command=lambda: self.handle_login(self.email, self.password))
        self.login_button.config(state="disabled", width=30)  # Button starts disabled
        self.login_button.grid(row=4, column=0, columnspan=4, pady=30)

        # Login error label
        self.error_label = tk.Label(self, text="Error logging in. Please try again.")
        self.error_label.configure(fg="red")

    # This function handles the login button
    def handle_login(self, email, password):
        # If the error label is present, remove it while we log in.
        self.error_label.grid_forget()

        # Call the login function from the database
        response = self.db.login(email.get(), password.get())

        if response["status"] == 200:  # If the response is 200
            self.controller.employee = response["employee_data"]  # Store employee data in the main app
            self.controller.frames["ReviewList"].refresh_employee_name()  # Call this function
            # From the review_list class so as to refresh the employee label
            self.controller.show_frame("ReviewList")  # go to the ReviewList frame
        else:  # otherwise
            self.error_label.grid(row=5, column=0, columnspan=4)  # Display error message.

    # This function is called each time a key is pressed on email or password.
    def on_input_change(self, *args):
        email_string = self.email.get()
        password_string = self.password.get()
        if email_string and password_string:
            # Enable the login button if both email and password exist.
            self.login_button.config(state="normal")
        else:
            self.login_button.config(state="disabled")




