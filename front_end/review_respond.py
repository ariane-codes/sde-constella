import tkinter as tk
import tkinter.font as tk_font
from datetime import datetime
from gmail.gmail import Gmail


class ReviewRespond(tk.Frame):
    def __init__(self, parent, db, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.db = db
        self.controller = controller

        # Setting column configure so everything is well spread horizontally
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=7)

        # Title
        title_font = tk_font.Font(family="Helvetica", size=18, weight="bold")
        self.title = tk.Label(self,
                              text=f"{self.controller.review_data['star_rating'] * '⭐'} "
                                    f"{controller.review_data['title']}",
                              wraplength=350,
                              justify="left")
        self.title.grid(row=0, column=0, columnspan=1, sticky=tk.EW, padx=5)
        self.title.configure(font=title_font, wraplength=450, justify="left")

        # This employee container has the employee name and the logout button.
        employee_container = tk.Frame(self)
        employee_container.grid(row=0, column=1, sticky=tk.EW, padx=5)

        employee_container.columnconfigure(0, weight=1)
        employee_container.columnconfigure(1, weight=1)
        employee_container.columnconfigure(2, weight=2)

        smaller_font = tk.font.Font(family="Helvetica", size=14, weight="bold")

        # Employee name
        self.employee_name_label = tk.Label(employee_container,
                                            text=f"{self.controller.employee['emp_first_name']} {self.controller.employee['emp_last_name']}")
        self.employee_name_label.grid(row=0, column=2, columnspan=1)
        self.employee_name_label.configure(font=smaller_font)

        # Logout button (simply display login page again)
        logout_button = tk.Button(employee_container, text="Logout",
                                  command=lambda: self.controller.show_frame("Login"))
        logout_button.grid(row=0, column=3, columnspan=1, sticky=tk.E)
        logout_button.config(width=15)

        # Review container
        self.review_frame = tk.Frame(self)
        self.review_frame.grid(row=1, column=0, sticky=tk.NS)

        # Configure rows and columns for this review frame
        self.review_frame.rowconfigure(0, weight=3)
        self.review_frame.rowconfigure(1, weight=3)
        self.review_frame.rowconfigure(2, weight=2)
        self.review_frame.columnconfigure(0, weight=1)
        self.review_frame.columnconfigure(0, weight=1)

        # A text widget to hold the review
        self.review_display = tk.Text(
            self.review_frame,
            bg="#E6E6E6",
            wrap="word",
            padx=20,
            width=60,
            height=2,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.review_display.insert(1.0, self.controller.review_data["body"])
        self.review_display.config(state="disabled")
        self.review_display.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        # Another text widget to hold the response by the CSR
        self.email_response = tk.Text(
            self.review_frame,
            wrap="word",
            padx=20,
            width=60,
            height=2,
            pady=10,

        )
        self.email_response.insert(1.0, "Type your response here...")
        self.email_response.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        # Back button
        self.back_button = tk.Button(
            self.review_frame,
            text="Go back",
            width=15,
            command=lambda: self.handle_go_back(),
            state="disabled"
        )
        self.back_button.grid(row=2, column=0, columnspan=1, sticky=tk.W, padx=5)

        # Send email button
        self.send_email_button = tk.Button(
            self.review_frame,
            text="Send",
            width=15,
            command=lambda: self.handle_send_email()
        )
        self.send_email_button.grid(row=2, column=1, columnspan=1, sticky=tk.E, padx=5)

        # Send email message (success/error)
        self.send_email_msg = tk.Label(
            self.review_frame,
            text=""
        )
        # I'll grid it after the email is sent.

        # Customer details container (right side column)
        right_side_frame = tk.Frame(self)
        right_side_frame.grid(row=1, column=1, columnspan=1, sticky=tk.NSEW)

        # Product and customer details
        product_font_bold = tk.font.Font(family="Helvetica", size=16, weight="bold")
        product_font_smaller = tk.font.Font(family="Helvetica", size=13)
        product_font_smaller_bold = tk.font.Font(family="Helvetica", size=13, weight="bold")

        self.product_name_label = tk.Label(
            right_side_frame,
            font=product_font_bold,
            text=self.controller.review_data["product_title"],
            wraplength=350,
            justify="left"
        )
        self.product_name_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky=tk.W)

        # Separating the word "Category: " to make it bold.
        _product_category = tk.Label(
            right_side_frame,
            font=product_font_smaller_bold,
            text="Category: "
        )
        _product_category.grid(row=1, column=0, padx=20, pady=2, sticky=tk.W)

        # Product category
        self.product_category_label = tk.Label(
            right_side_frame,
            font=product_font_smaller,
            text=self.controller.review_data["product_category"]
        )
        self.product_category_label.grid(row=1, column=1, padx=20, pady=2, sticky=tk.W)

        # Separating the word "Price: " to make it bold.
        _product_price = tk.Label(
            right_side_frame,
            font=product_font_smaller_bold,
            text="Price: "
        )
        _product_price.grid(row=2, column=0, padx=20, pady=2, sticky=tk.W)

        # Product price
        self.product_price_label = tk.Label(
            right_side_frame,
            font=product_font_smaller,
            text=f"£{self.controller.review_data['purchase_price']}"
        )
        self.product_price_label.grid(row=2, column=1, padx=20, pady=2, sticky=tk.W)

        # Separating the word "Date Purchased: " to make it bold.
        _date_purchased = tk.Label(
            right_side_frame,
            font=product_font_smaller_bold,
            text="Date purchased: "
        )
        _date_purchased.grid(row=3, column=0, padx=20, pady=2, sticky=tk.W)

        # Product price
        self.date_purchased_label = tk.Label(
            right_side_frame,
            font=product_font_smaller,
            text=self.controller.review_data["created"].strftime("%Y-%m-%d %H:%M")
        )
        self.date_purchased_label.grid(row=3, column=1, padx=20, pady=2, sticky=tk.W)

        # Customer details

        self.customer_name_label = tk.Label(
            right_side_frame,
            font=product_font_bold,
            text=self.controller.customer_data["name"]
        )
        self.customer_name_label.grid(row=4, column=0, columnspan=2, padx=20, pady=15, sticky=tk.W)

        # Separating the word "Premier Customer: " to make it bold.
        _premier_customer = tk.Label(
            right_side_frame,
            font=product_font_smaller_bold,
            text="Premier Customer: "
        )
        _premier_customer.grid(row=5, column=0, padx=20, pady=2, sticky=tk.W)

        # Product price
        self.premier_customer = tk.Label(
            right_side_frame,
            font=product_font_smaller,
            text="Yes" if self.controller.customer_data["premier"] == 1 else "No"
        )
        self.premier_customer.grid(row=5, column=1, padx=20, pady=2, sticky=tk.W)

        # Gift card button for 10
        self.gift_card_10 = tk.Button(
            right_side_frame,
            text="£10 Gift Card",
            width=15,
            command=lambda: self.handle_gift_card_10()
        )
        self.gift_card_10.grid(row=6, column=0, padx=20, pady=20)

        # Gift card button for 20
        self.gift_card_20 = tk.Button(
            right_side_frame,
            text="£20 Gift Card",
            width=15,
            command=lambda: self.handle_gift_card_20()
        )
        self.gift_card_20.grid(row=6, column=1, padx=10, pady=20)

        # Discount code button
        self.discount_button = tk.Button(
            right_side_frame,
            text="Discount Code",
            width=15,
            command=lambda: self.handle_discount_code()
        )
        self.discount_button.grid(row=7, column=0, padx=10, pady=10)

    def refresh_fields(self):
        # Refresh title contents
        self.title.config(text=f"{self.controller.review_data['star_rating'] * '⭐'} "
                               f"{self.controller.review_data['title']}")
        # Refresh employee name
        self.employee_name_label.config(
            text=f"{self.controller.employee['emp_first_name']} {self.controller.employee['emp_last_name']}")

        # Refresh review body
        self.review_display.config(state="normal")
        self.review_display.insert(1.0, self.controller.review_data["body"])
        self.review_display.config(state="disabled")

        # Refresh email response
        self.email_response.delete("1.0", tk.END)
        self.email_response.insert(1.0, "Type your response here...")

        # Refresh product title
        self.product_name_label.config(text=self.controller.review_data["product_title"])

        # Refresh product category
        self.product_category_label.config(text=self.controller.review_data["product_category"])

        # Refresh product price
        self.product_price_label.config(text=f"£{self.controller.review_data['purchase_price']}")

        # Refresh the product purchase date
        self.date_purchased_label.config(text=self.controller.review_data["created"].strftime("%Y-%m-%d %H:%M"))

        # Refresh the customer name
        self.customer_name_label.config(text=self.controller.customer_data["name"])

        # Refresh premier customer label
        self.premier_customer.config(text="Yes" if self.controller.customer_data["premier"] == 1 else "No")

        # Refresh states of buttons
        if self.controller.review_data["purchase_price"] >= 10:
            self.gift_card_10.config(state="normal")
        else:
            self.gift_card_10.config(state="disabled")

        if self.controller.review_data["purchase_price"] >= 20:
            self.gift_card_20.config(state="normal")
        else:
            self.gift_card_20.config(state="disabled")

        # Remove email message label
        self.send_email_msg.grid_remove()

        # Disable the back button
        self.back_button.config(state="disabled")

        # Enable the send button
        self.send_email_button.config(state="normal")

    def handle_send_email(self):

        gmail = Gmail()

        message_sent = gmail.send_email(
            recipient="ariane.ernandorena@gmail.com",
            text=self.email_response.get(1.0, tk.END),
            subject="Your Constella Review"
        )

        if message_sent == "Success":  # Message was sent successfully
            # Enable the go back button
            self.back_button.config(state="normal")
            # Display success message
            self.send_email_msg.config(
                text="Email sent successfully!",
                foreground="green",
            )
            self.send_email_msg.grid(row=3, column=1, columnspan=1, sticky=tk.E, padx=5)
            # Disable the send button to avoid double sending
            self.send_email_button.config(state="disabled")

        else:
            # Disable the go back button
            self.back_button.config(state="disabled")
            # Display error message
            self.send_email_msg.config(
                text="Error sending email",
                foreground="red",
            )
            self.send_email_msg.grid(row=3, column=1, columnspan=1, sticky=tk.E, padx=5)

    def handle_gift_card_10(self):
        # Add the message to the end of the email response box
        # and disable the other discount/gift card buttons
        self.email_response.insert(
            tk.END,
            "\nBecause of your trouble, we would like to offer a "
            "£10 gift card for you to enjoy in your future purchases"
            "at Constella. Just use this promo code in your next purchase:"
            " CONSTELLA10."
        )
        self.gift_card_10.config(state="disabled")
        self.gift_card_20.config(state="disabled")
        self.discount_button.config(state="disabled")

    def handle_gift_card_20(self):
        # Add the message to the end of the email response box
        # and disable the other discount/gift card buttons
        self.email_response.insert(
            tk.END,
            "\nBecause of your trouble, we would like to offer a "
            "£20 gift card for you to enjoy in your future purchases"
            "at Constella. Just use this promo code in your next purchase:"
            " CONSTELLA20."
        )
        self.gift_card_10.config(state="disabled")
        self.gift_card_20.config(state="disabled")
        self.discount_button.config(state="disabled")

    def handle_discount_code(self):
        # Add the message to the end of the email response box
        # and disable the other discount/gift card buttons
        self.email_response.insert(
            tk.END,
            "\nBecause of your trouble, we would like to offer a "
            "15% discount code for you to enjoy in your future purchases"
            "at Constella. Just use this promo code in your next purchase:"
            " CONSTELLA15."
        )
        self.gift_card_10.config(state="disabled")
        self.gift_card_20.config(state="disabled")
        self.discount_button.config(state="disabled")

    def handle_go_back(self):

        # We need to wipe the reviews in the ReviewList and reset them
        self.controller.frames["ReviewList"].refresh_review_list()

        # And then display the ReviewList
        self.controller.show_frame("ReviewList")
