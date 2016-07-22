
from ibuydeal.DB.database import json_response
from ibuydeal.Content.content import ContentList

static_path = '/home/ec2-user/static/'


class User:
    def __init__(self, userid='default'):
        self.id = userid

    @property
    def contents(self):
        contents_id = {46: 2, 29: 3, 34: 5, 24: 1, 25: 4}
        return contents_id

    def response(self):
        dbdata = ContentList(self.contents).info
        return json_response(dbdata)
