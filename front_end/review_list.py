import tkinter as tk
import tkinter.font as tk_font

from front_end.table import generate_table


class ReviewList(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.db = db
        self.controller = controller
        print("Initialising review list, getting initial reviews.")
        self.reviews = db.get_reviews(page_size=10, last_review_id=0)
        self.start = 0
        self.end = 9
        self.selected_review = None

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
        self.employee_name_label = tk.Label(self, text=f"{self.controller.employee['emp_first_name']} {self.controller.employee['emp_last_name']}")
        self.employee_name_label.grid(row=0, column=1, columnspan=1, sticky=tk.NS)
        self.employee_name_label.configure(font=employee_name_font)

        # Logout button (simply display login page again
        logout_button = tk.Button(self, text="Logout",
                                  command=lambda: self.controller.show_frame("Login"))
        logout_button.grid(row=0, column=2, columnspan=1, sticky=tk.E, padx=20)
        logout_button.config(width=15)

        # A subframe contains the table and the next/back buttons
        table_container_frame = tk.Frame(self)
        table_container_frame.grid(row=1, column=0, columnspan=3, sticky=tk.EW)

        # This subframe will have only 2 columns with the same weight.
        table_container_frame.columnconfigure(0, weight=1)
        table_container_frame.columnconfigure(1, weight=1)

        # Generate table
        self.table = generate_table(table_container_frame)

        # Insert the reviews in the table
        self.insert_reviews(0, 9)

        # Add the table to the grid in the table container frame
        self.table.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=15)

        # Adding previous_button to "self" so I can enable it when user clicks next.
        self.previous_button = tk.Button(
            table_container_frame,
            text="Previous",
            state="disabled",
            width=20,
            command=lambda: self.handle_previous()
        )
        self.previous_button.grid(row=1, column=0, padx=15, pady=20, sticky=tk.W)

        next_button = tk.Button(
            table_container_frame,
            text="Next",
            width=20,
            command=lambda: self.handle_next()
        )
        next_button.grid(row=1, column=1, padx=15, pady=20, sticky=tk.E)

        # Bind the Treeview Select event to the on_select function
        self.table.bind("<<TreeviewSelect>>", self.on_select)

        # Go to review button
        self.go_to_review_button = tk.Button(
            self,
            text="Go to review",
            state="disabled",
            width=15,
            command=lambda: self.handle_go_to_review()
        )
        self.go_to_review_button.grid(row=2, column=2, columnspan=1, sticky=tk.E, padx=20)

    def fetch_reviews(self, last_review_id):
        self.reviews += self.db.get_reviews(page_size=10, last_review_id=last_review_id)

    def insert_reviews(self, start_index, end_index):
        # Insert the reviews in the table
        for index, r in enumerate(
                self.reviews[start_index:end_index+1]  # Only those reviews that
                # are between the indexes.
        ):
            # We need to modify the review as it comes to fit the treeview
            # When it gets converted to a tuple
            review_modified_dictionary = {
                "review_id": r["review_id"],
                "review_created": r["review_created"],
                "review_star_rating": r["review_star_rating"],
                "premier_customer": "Yes" if r["review_customer_premier"] == 1 else "No",
                "review_title": r["review_title"],
                "review_product_category": r["review_product_category"],
                "review_purchase_price": f"${r['review_purchase_price']}"
            }
            # Convert the dictionary into a tuple
            review_tuple = tuple(review_modified_dictionary.values())

            # Insert into the table
            if index % 2 == 0:  # it's an even row
                self.table.insert("", tk.END, values=review_tuple)
            else:  # it's an odd row, add a tag so the table knows it needs to color it.
                self.table.insert("", tk.END, values=review_tuple, tags=("odd_row",))

    def handle_next(self):
        # Check if we already loaded those reviews. We don't want to load them unnecessarily.
        if len(self.reviews) <= self.end + 1:
            # We don't have the "next" reviews, we'll need to call the db and load more.
            print("Getting more reviews")
            self.fetch_reviews(last_review_id=self.reviews[-1]["review_id"])

        # Now we've made sure we got the reviews, we can go ahead and display the next page.

        # We do this by DELETING the existing rows
        self.table.delete(*self.table.get_children())

        # Move the page markers 10 reviews forward
        self.start += 10
        self.end += 10

        # And populate the table with the new reviews
        self.insert_reviews(self.start, self.end)

        self.previous_button.config(state="normal")

    def handle_previous(self):
        # We will always have the "previous" reviews, so no need to refetch anything.
        # Similar to handle_next, but we'll subtract 10.

        self.table.delete(*self.table.get_children())
        self.start -= 10
        self.end -= 10
        self.insert_reviews(self.start, self.end)

        if self.start <= 0:
            self.previous_button.config(state="disabled")

    def refresh_employee_name(self):
        # This is called in the login screen
        # And resets the employee name.
        self.employee_name_label.config(text=f"{self.controller.employee['emp_first_name']} {self.controller.employee['emp_last_name']}")

    def on_select(self, event):
        self.selected_review = self.table.item(event.widget.selection())["values"][0]
        self.go_to_review_button.config(state="normal")

    def handle_go_to_review(self):
        self.controller.selected_review = self.selected_review
        self.controller.show_frame("ReviewRespond")
