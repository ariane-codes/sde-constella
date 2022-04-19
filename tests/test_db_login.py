import sys, os
# enables accessing class functions from other directories (UNIT 8 - Creating Libraries)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.database import Database

db = Database()

def test_login_success():
    """ database successful login function test """
    login_result = db.login('natalie.smith@constella.com', 'C0n$t3ll4')
    assert login_result['status'] == 200
    assert login_result['message'] == "Login successful"

def test_login_incorrect_username():
    """ database unsuccessful login function test for incorrect username"""
    login_result=db.login('paolasz@constella.com', 'C0n$t3ll4')
    assert login_result["status"] == 400
    assert login_result["message"] == "Incorrect email or password"

def test_login_incorrect_password():
    """ database unsuccessful login function test for incorrect password"""
    login_result=db.login('natalie.smith@constella.com', 'invalidPassword')
    assert login_result["status"] == 400
    assert login_result["message"] == "Incorrect email or password"
