import tkinter as tk
from datetime import datetime

from front_end.login import Login
from front_end.review_list import ReviewList
from front_end.review_respond import ReviewRespond
from database.database import Database


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Constella - Review Management")
        self.geometry("900x700")
        self.resizable(False, False)

        self.db = Database()
        self.employee = {
            "emp_first_name": "Dummy",
            "emp_last_name": "Name",
            "emp_id": None
        }
        self.selected_review = None

        # self.review_data & self.customer_data are populated in
        # ReviewList after db.assign_review() is called
        # THIS IS DUMMY DATA
        self.review_data = {
            "id": 1234,
            "product_title": "A baby swing lalala lalala lalala lalal lalalala lalalal lala la",
            "product_category": "Dummy Category",
            "star_rating": 2,
            "status": "NEW",
            "title": "This swing did not help my daughter at all. ... A baby swing lalala lalala lalala lalal lalalala lalalal lala la",
            "body": "This swing did not help my daughter at all.  Put her in it multiple times for 3 months with no success, the longest she sat unit was 20 min.  Get a regular swing.",
            "purchase_price": 7.03,
            "created": datetime.strptime("2022-02-24 16:27:17", "%Y-%m-%d %H:%M:%S"),
            "customer_id": 1152,
            "employee_id": 1
        }
        self.customer_data = {
            "id": 1152,
            "name": "Naoko Matsuda",
            "email": "N.Matsuda363@example.com",
            "join_date": datetime.strptime("2020-07-20 06:21:34", "%Y-%m-%d %H:%M:%S"),
            "premier": 1
        }

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


if __name__ == '__main__':

    app = Application()
    app.mainloop()
