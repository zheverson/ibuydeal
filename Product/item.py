from ibuydeal.DB.database import cursor, dictcursor, json_response
from ibuydeal.Content.media import image_ratio, image_path


class Item:
    def __init__(self, itemid):
        self.id = itemid

    @property
    def product_info(self):
        with cursor() as cur:
            cur.execute(
                "SELECT item.product, brand.name, product.name FROM item, product, brand "
                "WHERE brand.id=product.brand and item.product=product.id and item.id=%s",
                (self.id,)
            )
            data = cur.fetchone()
        dictdata = {"brand": data[1], "product": data[0], "name": data[2]}
        return dictdata

    @property
    def product_image_path(self):
        return image_path + 'item/' + str(self.id) + '/product'

    @property
    def color_image_path(self):
        return image_path + 'item/' + str(self.id) + '/color'

    @property
    def basic_info(self):
        info = self.item_info
        info.update(self.product_info)
        return info

    # price, image ratio and item id
    @property
    def item_info(self):
        with dictcursor() as cur:
            cur.execute(
                "SELECT item.id, item.price, item.color FROM item WHERE item.id=%s",
                (self.id,))
            data = cur.fetchone()
        data["ratio"] = image_ratio(self.product_image_path)
        return data

    @property
    def contents(self):

        with dictcursor() as cur:
            cur.execute(
                "SELECT creator.name,content.title,content.id FROM creator,content WHERE content.id in (SELECT content_id FROM content_item WHERE content_item.id in (SELECT contenttime_id FROM contenttime_item WHERE item_id=%s) GROUP BY content_id) and creator.id = content.creator_id",
                (self.id,))
            dbtuple = cur.fetchall()
        return dbtuple
    
    def response(self, para):
        if para == 'info':
            return json_response(self.basic_info)
        elif para == 'contents':
            return json_response(self.contents)
