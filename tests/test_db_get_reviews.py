import sys, os
# enables accessing class functions from other directories (UNIT 8 - Creating Libraries)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.database import Database

db = Database()

def test_get_reviews(db_connect):
    """ database successful review retrieval test """

    mydb = db_connect
    mycursor = mydb.cursor()

    # Default parameters
    stars = 3
    page_size = 5

    sql = "SELECT r.*, c.premier FROM review r LEFT JOIN customer c \
                ON r.customer_id = c.id WHERE r.employee_id IS NULL AND r.star_rating \
                <= %s ORDER BY r.id DESC LIMIT %s"
    vals = (stars, page_size)
    mycursor.execute(sql, vals)
    result = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    reviews = []
    for row in result:
        temp_dict = {"review_id" : row[0],
                    "review_product_title" : row[1],
                    "review_product_category" : row[2],
                    "review_star_rating" : row[3],
                    "review_status" : row[4],
                    "review_title" : row[5],
                    "review_body" : row[6],
                    "review_purchase_price" : row[7],
                    "review_created" : row[8],
                    "review_customer_id" : row[9],
                    "review_employee_id" : row[10],
                    "review_customer_premier": row[11]
                    }
        reviews.append(temp_dict)    
    assert reviews == db.get_reviews()

def test_get_reviews_page_size():
    """ The function tests that the correct number of reviews are returned
    for the default value and when a value is passed """

    assert len(db.get_reviews()) == 5
    assert len(db.get_reviews(page_size=7)) == 7

def test_get_reviews_star_rating():
    """ The function tests that all returned reviews have 3 stars or less """

    for each in db.get_reviews():
        assert each['review_star_rating'] <= 3

def test_get_reviews_order_desc():    
    """ This function tests that reviews are sorted by created date in descending order """

    reviews = db.get_reviews()
    for index, each in enumerate(reviews):
        if index < len(reviews):
            j = index + 1
            # Compare current iteration review date to remaining reviews in the list
            while j < len(reviews):
                assert each['review_created'] > reviews[j]['review_created']
                j+=1

def test_get_reviews_pagination(db_connect):
    """ This function tests pagination to ensure that the next page of 
    reviews do not duplicate any of the reviews on the current page """

    mydb = db_connect
    mycursor = mydb.cursor()
    # Default parameters
    stars = 3
    page_size = 5
    # Get first page of reviews
    sql = "SELECT r.*, c.premier FROM review r LEFT JOIN customer c \
        ON r.customer_id = c.id WHERE r.employee_id IS NULL AND r.star_rating \
        <= %s ORDER BY r.id DESC LIMIT %s"
    vals = (stars, page_size)
    mycursor.execute(sql, vals)
    reviews = mycursor.fetchall()
    # Create a list of review ids from the first page
    review_ids = []
    for review in reviews:
        review_ids.append(review[0])
    # Store the last review ID to be used for pagination
    last_review_id = review_ids[len(review_ids)-1]
    # Get the next page of reviews
    sql = "SELECT r.*, c.premier FROM review r LEFT JOIN customer c \
        ON r.customer_id = c.id WHERE r.employee_id IS NULL AND r.star_rating \
        <= %s AND r.id < %s ORDER BY r.id DESC LIMIT %s"
    vals = (stars, last_review_id, page_size)
    mycursor.execute(sql, vals)
    next_reviews = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    # Create a list of review ids from the second page
    next_review_ids = []
    for review in next_reviews:
        next_review_ids.append(review[0])
    # Compare each review id in the first page to each
    # review in the second page
    for review_id in review_ids:
        for next_review_id in next_review_ids:
            assert review_id != next_review_id

def test_get_reviews_unassigned():
    """ This function tests a large sample of returned reviews to ensure that
    all returned reviews are not already assigned to an employee"""

    reviews = db.get_reviews(page_size=100)

    for review in reviews:
        assert review['review_employee_id'] is None

