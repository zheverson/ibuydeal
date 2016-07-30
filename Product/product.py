from ibuydeal.DB.database import cursor, json_response
from ibuydeal.Product.item import Item


class Product:
    def __init__(self, id):
        self.id = id

    # return [item_id1, item_id2, ...]
    @property
    def items_id(self):
        with cursor() as cur:
            cur.execute("SELECT item.id FROM item WHERE item.product=%s", (self.id,))
            data = cur.fetchall()

        return [i[0] for i in data]

    # return [{itemid:1, brand: '', price: ''}]
    @property
    def items_info(self):
        return [Item(i).basic_info for i in self.items_id]

    def response(self, request):
        if request == "items":
            return json_response(self.items_info)
