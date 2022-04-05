import sys, os
# enables accessing class functions from other directories (UNIT 8 - Creating Libraries)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
from database.database import Database

class TestDBFunctions(unittest.TestCase):
    """ Testing class containing tests for all Database class methods"""
    def test_login(self):
        """ database login function test """
        dbase = Database()
        actual = dbase.login('natalie.smith', 'C0n$t3ll4')
        expected = {"status": 200, "message": "Login successful"}
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
