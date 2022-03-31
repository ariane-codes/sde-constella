import tkinter as tk


# I'm using an OOP approach for this app.
# Check this Stack Overflow answer:
# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application/17470842#17470842

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Initialize rest of the GUI here.
        greeting = tk.Label(text="Hello world!")
        greeting.pack()

<<<<<<< Updated upstream
=======
    # Initial Testing code
    db=Database()
    reviews = db.get_reviews()
    for review in reviews:
        print(str(review['review_created']) + "  " + review['review_title'] + "  " + str(review['review_star_rating']))
    response = db.login('natalie.smith', 'C0n$t3ll4')
    print("Status: " + str(response['status']))
    print("Message: " + str(response['message']))

>>>>>>> Stashed changes

# Try running this!
if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
