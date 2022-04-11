from tkinter import ttk
import tkinter as tk


def generate_table(parent_for_table):

    # General styling for the table
    style = ttk.Style(parent_for_table)
    style.theme_use("clam")
    style.configure("Treeview", rowheight=40)
    style.configure("Treeview.Heading", background="#45716b", foreground="white")

    # Define the columns for the table. They need to be the same as the data
    # that comes from the database.
    table_columns = (
        "review_created",
        "review_star_rating",
        "review_customer_id",
        "review_title",
        "review_product_category",
        "review_purchase_price"
    )

    # Create the table using Treeview
    table = ttk.Treeview(
        parent_for_table,
        columns=table_columns,
        show="headings"
    )

    # Define the headings -- how you want the columns to be displayed.
    table.heading("review_created", text="Date")
    table.heading("review_star_rating", text="Stars")
    table.heading("review_customer_id", text="Customer ID")
    table.heading("review_title", text="Title")
    table.heading("review_product_category", text="Product Category")
    table.heading("review_purchase_price", text="Price", anchor="center")

    # Column styling
    table.column("review_created", minwidth=10, anchor="center")
    table.column("review_star_rating", width=60, anchor="center")
    table.column("review_customer_id", width=100, anchor="center")
    table.column("review_title", anchor=tk.W)
    table.column("review_product_category", anchor="center")
    table.column("review_purchase_price", stretch=False, width=100, anchor="center")

    # Configure alternating colours
    table.tag_configure("odd_row", background="#B8C5C3")

    return table
