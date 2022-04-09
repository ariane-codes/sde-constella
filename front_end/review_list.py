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
        font = tk_font.Font(family="Helvetica", size=24, weight="bold")
        title = tk.Label(self, text="Review List")
        title.grid(row=0, column=0, columnspan=1, sticky=tk.W, padx=30, pady=45)
        title.configure(font=font)