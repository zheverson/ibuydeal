import psycopg2
from PIL import Image
import simplejson as json
import glob
import decimal

static_path = '/home/ec2-user/static/'

def dbcon():
    con = psycopg2.connect("dbname='newapp' password='8326022' user='ec2-user' host='localhost'")
    return con
        
def image_ratio(path):
    path1 = glob.glob(path + '*')
    assert path1, path
    image = Image.open(path1[0])
    return float(format(image.size[0]/image.size[1],'.6f'))

class User:
    def __init__(self,id='default'):
        self.id = id

    def get_contents(self):
        contents_id = (25,29,34,45,24)
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
        dbjson = json.dumps([{"id":i[0], "ratio": image_ratio(glob.glob('/home/ec2-user/static/image/' + vImage + str(i[0])+'.*')[0]) , "title": i[1], "name": i[2]} for i in dbdata])
        return dbjson.encode('utf-8')


class Video_Content:

    def __init__(self,id):
        self.id = id

    def get_itemtimes(self):
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT id,display_time FROM content_item WHERE content_id=%s",(self.id,))
        dbtuple = cur.fetchall()
        con.close()
        return dbtuple

    def sort_time(self):
        times = self.get_itemtimes()
        times.sort(key=lambda x:int(x[1].split('-')[0]))
        timeline = self.timeline(times)
        items = []
        con = dbcon()
        cur = con.cursor()
        for i in times:
            cur.execute("SELECT item_id FROM contenttime_item WHERE contenttime_id=%s",(i[0],))
            item_section = []
            for j in cur.fetchall():
                item = Item(j[0])
                iteminfo = item.get_basic_info()
                iteminfo["ratio"] = image_ratio(item.product_image_path())
                item_section.append(iteminfo)
            items.append(item_section)
                            
        item_time = {'items':items,'timeline':timeline}
        con.close()
        return item_time
    
    def ratioForID(self,index):
        item = Item(index)
        return image_ratio(item.product_image_path) 

    def timeline(self,dbdata):
        splitdata = [i[1].split('-') for i in dbdata]
        timeline = []
        [timeline.extend(i) for i in splitdata]
        int_timeline = [int(i) for i in timeline]
        return int_timeline

    def response(self, a):
        if a == "items":
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
    con.close()
    return '&#'.join(db_tuple).encode('utf-8')

class Item:
    def __init__(self,id):
        self.id = id

    def product_image_path(self):
        return static_path + 'image/item/' + str(self.id) + '/product'
        

    def color_image_path(self):
        return static_path + 'image/item/' + str(self.id) + '/color'

    def get_basic_info(self):
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT brand.name,product.name,item.price FROM brand,product,item WHERE item.product=product.id and product.brand=brand.id and item.id=%s",(self.id,))
        data = cur.fetchall()
        brand = data[0][0]
        name = data[0][1]
        price = data[0][2]
        con.close()
        return {"id":self.id,"brand":brand,"name":name,"price":price}
    
    def get_all_colors(self):
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT id,color FROM item WHERE item.id in (SELECT item.id FROM item WHERE item.product=(SELECT product FROM item WHERE id=%s))",(self.id,))
        data = cur.fetchall()
        return data
        
    def response(self,a):
        if a == 'colors':
            jsondata = json.dumps(self.get_all_colors())
            return jsondata.encode('utf-8')
