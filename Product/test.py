import unittest
from ibuydeal.Product.item import Item
from ibuydeal.Product.product import Product


class ItemTest(unittest.TestCase):
    def setUp(self):
        self.item = Item(77)

    def testInfo(self):
        assert self.item.basic_info['brand'] == 'L.A. Girl'
        assert self.item.basic_info['productid'] == 16

    def testContent(self):
        assert self.item.contents[0]['id'] == 24


class ProductTest(unittest.TestCase):
    def setUp(self):
        self.product = Product(16)

    def testItems(self):
        assert self.product.items_info[0]['productid'] == 16

if __name__ == '__main__':
    unittest.main()
