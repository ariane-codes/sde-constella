import tkinter as tk


class ReviewRespond(tk.Frame):
    def __init__(self, parent, db, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.db = db
        self.controller = controller

        # Initialize rest of the GUI here.
        greeting = tk.Label(self, text="Hello respond to review!")
        greeting.pack(side="top", fill="x", pady=10)