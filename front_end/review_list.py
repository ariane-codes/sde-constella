import tkinter as tk
import tkinter.font as tk_font


class ReviewList(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.db = db
        self.controller = controller

        # Setting column configure so everything is well spread horizontally
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Title
        title_font = tk_font.Font(family="Helvetica", size=24, weight="bold")
        title = tk.Label(self, text="Review List")
        title.grid(row=0, column=0, columnspan=1, sticky=tk.W, padx=30, pady=45)
        title.configure(font=title_font)

        # Employee name
        employee_name_font = tk.font.Font(family="Helvetica", size=16, weight="bold")
        employee_name_label = tk.Label(self, text=self.controller.employee["name"])
        employee_name_label.grid(row=0, column=1, columnspan=1, sticky=tk.NS)
        employee_name_label.configure(font=employee_name_font)

        # Logout button (simply display login page again
        logout_button = tk.Button(self, text="Logout",
                                  command=lambda: self.controller.show_frame("Login"))
        logout_button.grid(row=0, column=2, columnspan=1)
        logout_button.config(width=15)