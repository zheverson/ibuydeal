import unittest
from ibuydeal.User.user import User


class UserTest(unittest.TestCase):
    def testUser(self):
        User().response()

if __name__ == '__main__':
    unittest.main()
