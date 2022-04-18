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
