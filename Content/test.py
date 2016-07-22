import  unittest
from content import VideoContent, ContentList

class ContentTest(unittest.TestCase)
    def setUp(self):

    def testContentList(self):
        cl = ContentList({46: 2, 29: 3, 34: 5, 24: 1, 25: 4})
        assert cl.info[0]['id'] == 24



