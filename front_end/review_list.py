import tkinter as tk


class ReviewList(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Initialize rest of the GUI here.
        greeting = tk.Label(text="Hello review list!")
        greeting.pack()