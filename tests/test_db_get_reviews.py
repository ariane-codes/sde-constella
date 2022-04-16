import sys, os
# enables accessing class functions from other directories (UNIT 8 - Creating Libraries)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.database import Database

db = Database()

def test_get_reviews():
    """ database successful review retrieval test """
    
    assert db.login('natalie.smith', 'C0n$t3ll4') == {"status": 200, "message": "Login successful"}
