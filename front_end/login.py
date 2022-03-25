import tkinter as tk


class Login(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Initialize rest of the GUI here.
        greeting = tk.Label(text="Hello login!")
        greeting.pack()