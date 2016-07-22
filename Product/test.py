import unittest
from item import Item
from Product import Product

class ItemTest(unittest.TestCase):
    def setUp(self):
        self.item = Item(77)

    def testInfo(self):
        assert self.item.basic_info['brand'] == 'L.A. Girl'

    def testContent(self):
        assert self.item.contents[0]['id'] == 24


class ProductTest(unittest.TestCase):
    def setUp(self):
        self.product = Product(16)

    def testInfo(self):
        assert self.product.info['brand'] == 'L.A. Girl'

    def testColors(self):
        assert self.product.colors[77] == 'White,GEB19'

if __name__ == '__main__':
    unittest.main()
