import unittest
from ibuydeal.Content.content import ContentList


class ContentTest(unittest.TestCase):

    def testContentList(self):
        cl = ContentList({46: 2, 29: 3, 34: 5, 24: 1, 25: 4})
        assert cl.info[0]['id'] == 24

if __name__ == '__main__':
    unittest.main()
