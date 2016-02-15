import psycopg2
from PIL import Image
import json
import glob

def dbcon():
    con = psycopg2.connect("dbname='newapp' password='8326022' user='ec2-user' \
host='localhost'")
    return con
        
def image_ratio(subpath):
    folder = '/home/ec2-user/static/image/video_thumbnail/mobile/'
    image = Image.open(glob.glob(folder+subpath+'*')[0])
    return float(format(image.size[0]/image.size[1],'.6f'))

class User:
    def __init__(self,id='default'):
        self.id = id

    def get_contents(self):
        contents_id = (25,29,34,45)
        return contents_id

    def db_values(self):
        con = dbcon()
        cur = con.cursor()
        contents_id = self.get_contents()
        cur.execute("SELECT content.id,title,name FROM content,creator WHERE content.creator_id=creator.id and content.id IN %s;",(contents_id,))
        dbtuple = cur.fetchall()
        con.close()
        return dbtuple

    def response(self):
        dbdata = self.db_values()
        dbjson = json.dumps([{"id":str(i[0]), "ratio": image_ratio(str(i[0])) , "title": i[1], "name": i[2]} for i in dbdata])
        return dbjson.encode('utf-8')


        
