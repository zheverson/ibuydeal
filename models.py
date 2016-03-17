import psycopg2
from PIL import Image
import json
import glob
import decimal

def dbcon():
    con = psycopg2.connect("dbname='newapp' password='8326022' user='ec2-user' host='localhost'")
    return con
        
def image_ratio(path):
    image = Image.open(path)
    return float(format(image.size[0]/image.size[1],'.6f'))

def image_path(imageID):
    mainPath = '/home/ec2-user/static/image/'
    return glob.glob(mainPath + 'item/'+str(imageID)+'/'+str(imageID)+'.*')[0]

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
        vImage = 'video_thumbnail/mobile/'
        dbjson = json.dumps([{"id":str(i[0]), "ratio": image_ratio(glob.glob('/home/ec2-user/static/image/' + vImage + str(i[0])+'.*')[0]) , "title": i[1], "name": i[2]} for i in dbdata])
        return dbjson.encode('utf-8')


class Content:

    def __init__(self,id):
        self.id = id

    def get_itemtimes(self):
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT item_id,display_time FROM content_item WHERE content_id=%s",(self.id,))
        dbtuple = cur.fetchall()
        con.close()
        return dbtuple

    def sort_time(self):
        dbdata = self.get_itemtimes()
        dbdata.sort(key=lambda tup:tup[1])
        timeline = []
        items = []
        imagePath = 'item/'
        try:
            for index,value in enumerate(dbdata):
                timeline.extend([int(j[:2])*60+int(j[-2:]) for j in value[1].split(',')])
                path = image_path(value[0]) 
                items.append([(value[0], image_ratio(path))])
                while value[1]==dbdata[index+1][1]:
                    path = image_path(dbdata[index+1][0])
                    items[-1].append((dbdata[index+1][0],image_ratio(path)))
                    del dbdata[index+1]
        except IndexError:
            pass
        
        item_time = {'items':items,'timeline':timeline}
        return item_time

    def response(self):
        item_time = self.sort_time()
        json_item = json.dumps(item_time)
        return json_item.encode('utf-8')


def db_data(table, pkey,*args):
    con = dbcon()
    cur = con.cursor()
    cur.execute("""SELECT {} FROM {} WHERE id=%s;""".format(','.join(args),table),(pkey,))
    db_tuple = list(cur.fetchone())
    for index,i in enumerate(db_tuple):
        if not isinstance(i,str):
            db_tuple[index] = str(i)
    return '&#'.join(db_tuple).encode('utf-8')


        
