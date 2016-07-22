from ibuydeal.database import cursor, json_response

class Product:
    def __init__(self, id):
        self.id = id

    # return {int:string} {itemID:Color}
    @property
    def colors(self):
        cur = cursor()
        cur.execute(
                "SELECT id,color FROM item WHERE item.id in (SELECT item.id FROM item WHERE item.product=%s)",
                (self.id,))
        data = cur.fetchall()

        return {i[0]: i[1] for i in data}

    # return {string:string} {brand,name}
    @property
    def info(self):
        cur = cursor()
        cur.execute(
            "SELECT brand.name,product.name FROM brand,product WHERE product.brand=brand.id and product.id=%s",
            (self.id,))
        data = cur.fetchone()
        return {'brand': data[0], 'name': data[1]}

    def response(self, request):
        if request == "colors":
            return json_response(self.colors)
        elif request == "info":
            return json_response(self.info)
