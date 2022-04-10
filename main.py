import tkinter as tk
from front_end.login import Login
from front_end.review_list import ReviewList
from front_end.review_respond import ReviewRespond
from database.database import Database


# I'm using an OOP approach for this app.
# Check this Stack Overflow answer:
# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application/17470842#17470842


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Constella - Review Management")
        self.geometry("900x700")
        self.resizable(False, False)

        self.db = Database()
        self.employee = {}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, ReviewList, ReviewRespond):
            page_name = F.__name__
            frame = F(parent=container, controller=self, db=self.db)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def test_login(self):
        # Database testing code 
        response = self.db.login('natalie.smith', 'C0n$t3ll4')
        print("Status: " + str(response['status']))
        print("Message: " + str(response['message']))

    def test_get_reviews(self):
        reviews = self.db.get_reviews()
        for review in reviews:
            print(str(review['review_created']) + "  " + review['review_title'] + "  " + str(review['review_star_rating']))





# Try running this!
if __name__ == '__main__':

    app = Application()
    app.mainloop()
