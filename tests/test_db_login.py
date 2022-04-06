import sys, os
# enables accessing class functions from other directories (UNIT 8 - Creating Libraries)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.database import Database

db = Database()

def test_login_success():
    """ database successful login function test """
    assert db.login('natalie.smith', 'C0n$t3ll4') == {"status": 200, "message": "Login successful"}

def test_login_incorrect_username():
    """ database unsuccessful login function test for incorrect username"""
    assert db.login('invalid.user', 'C0n$t3ll4') ==\
    {"status": 400, "message": "Incorrect username or password"}

def test_login_incorrect_password():
    """ database unsuccessful login function test for incorrect password"""
    assert db.login('natalie.smith', 'invalidPassword') ==\
    {"status": 400, "message": "Incorrect username or password"}
