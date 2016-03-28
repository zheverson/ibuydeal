from database import cursor, dictcursor
from media import image_ratio, image_path
from database import json_response


class Item:
    def __init__(self, itemid):
        self.id = itemid

    def product_image_path(self):
        return image_path + 'item/' + str(self.id) + '/product'

    def color_image_path(self):
        return image_path + 'item/' + str(self.id) + '/color'

    def get_basic_info(self):
        cur = cursor()
        cur.execute(
            "SELECT brand.name,product.name,item.price FROM brand,product,item WHERE item.product=product.id and product.brand=brand.id and item.id=%s",
            (self.id,))
        data = cur.fetchall()
        brand = data[0][0]
        name = data[0][1]
        price = data[0][2]
        return {"id": self.id, "brand": brand, "name": name, "price": price,
                "ratio": image_ratio(self.product_image_path())}

    def get_all_colors(self):

        cur = cursor()
        cur.execute(
            "SELECT id,color FROM item WHERE item.id in (SELECT item.id FROM item WHERE item.product=(SELECT product FROM item WHERE id=%s))",
            (self.id,))
        data = cur.fetchall()
        return data

    def get_contents(self):

        cur = dictcursor()
        cur.execute(
            "SELECT creator.name,content.title,content.id FROM creator,content WHERE content.id in (SELECT content_id FROM content_item WHERE content_item.id in (SELECT contenttime_id FROM contenttime_item WHERE item_id=%s) GROUP BY content_id) and creator.id = content.creator_id",
            (self.id,))
        dbtuple = cur.fetchall()
        return dbtuple

    def response(self, a):
        if a == 'colors':
            return json_response(self.get_all_colors())
        if a == 'contents':
            from content import VideoContentList
            dbdata = self.get_contents()
            dbdata1 = VideoContentList(dbdata).add_content_thumbratio()
            return json_response(dbdata1)
