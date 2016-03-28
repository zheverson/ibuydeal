
from database import dictcursor
from database import json_response
from content import VideoContentList

static_path = '/home/ec2-user/static/'


class User:
    def __init__(self, userid='default'):
        self.id = userid

    def get_contents(self):
        contents_id = (45, 29, 34, 24, 25)
        return contents_id

    def get_contents_info(self):
        cur = dictcursor()
        contents_id = self.get_contents()
        cur.execute(
            "SELECT content.id,title,name FROM content,creator WHERE content.creator_id=creator.id and content.id IN %s;",
            (contents_id,))
        dbtuple = cur.fetchall()
        dbtuple.sort(key=self.feed_order)
        return dbtuple

    def feed_order(self, value):
        stupid = {45: 1, 29: 2, 34: 3, 24: 4, 25: 5}
        return stupid[value['id']]

    def response(self):
        dbdata = self.get_contents_info()
        dbdata1 = VideoContentList(dbdata).add_content_thumbratio()
        return json_response(dbdata1)
