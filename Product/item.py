from ibuydeal.database import cursor, dictcursor, json_response
from ibuydeal.media import image_ratio, image_path
import Product


class Item:
    def __init__(self, itemid):
        self.id = itemid
        self._product_id = None

    @property
    def product_id(self):
        if self._product_id is None:
            cur = cursor()
            cur.execute("SELECT item.product FROM item WHERE item.id=%s",(self.id,))
            data = cur.fetchone()
            self._product_id = data[0]
        return self._product_id

    @property
    def product_image_path(self):
        return image_path + 'item/' + str(self.id) + '/product'

    @property
    def color_image_path(self):
        return image_path + 'item/' + str(self.id) + '/color'

    @property
    def basic_info(self):
        info = self.__item_info
        product = Product(self.product_id)
        return info.update(product.get_info())

    # price, image ratio and item id
    @property
    def __item_info(self):
        cur = cursor()
        cur.execute(
            "SELECT item.price FROM item WHERE item.id=%s",
            (self.id,))
        data = cur.fetchone()
        price = data[0]
        return {"id": self.id, "price": price,
                "ratio": image_ratio(self.product_image_path)}

    @property
    def contents(self):

        cur = dictcursor()
        cur.execute(
            "SELECT creator.name,content.title,content.id FROM creator,content WHERE content.id in (SELECT content_id FROM content_item WHERE content_item.id in (SELECT contenttime_id FROM contenttime_item WHERE item_id=%s) GROUP BY content_id) and creator.id = content.creator_id",
            (self.id,))
        dbtuple = cur.fetchall()
        return dbtuple

    def response(self, a):
        if a == 'contents':
            from content import VideoContentList
            dbdata = self.contents
            dbdata1 = VideoContentList(dbdata).add_content_thumbratio()
            return json_response(dbdata1)
