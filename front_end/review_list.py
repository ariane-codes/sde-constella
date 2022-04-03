import tkinter as tk


class ReviewList(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.db = db
        self.controller = controller

        # Initialize rest of the GUI here.
        greeting = tk.Label(self, text="Hello review list!")
        greeting.pack(side="top", fill="x", pady=10)