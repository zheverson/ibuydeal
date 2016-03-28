from database import dictcursor
from media import image_ratio, image_path
import simplejson as json
from item import Item


class VideoContent:
    def __init__(self, videoid):
        self.id = videoid

    def get_itemtimes(self):
        cur = dictcursor()
        cur.execute("SELECT display_time,ARRAY_AGG(item_id) as items FROM content_item,contenttime_item WHERE content_id=%s and content_item.id=contenttime_item.contenttime_id GROUP BY content_item.id", (self.id,))
        dbtuple = cur.fetchall()
        return dbtuple

    def sort_time(self):
        times = self.get_itemtimes()
        times.sort(key=lambda x: int(x['display_time'].split('-')[0]))
        timeline = self.timeline(times)
        items = []
        for i in times:
            items.append([Item(j).get_basic_info() for j in i['items']])

        item_time = {'items': items, 'timeline': timeline}
        return item_time

    def thumb_path(self, platform):
        return image_path + 'video_thumbnail/' + platform + '/' + str(self.id)

    def timeline(self, dbdata):
        splitdata = [i['display_time'].split('-') for i in dbdata]
        timeline = []
        [timeline.extend(i) for i in splitdata]
        int_timeline = [int(i) for i in timeline]
        return int_timeline

    def response(self, a):
        if a == "items":
            item_time = self.sort_time()
            json_item = json.dumps(item_time)
            return json_item.encode('utf-8')


class VideoContentList:
    def __init__(self, dbarray):
        # list of dictionary
        self.contents = dbarray

    def add_content_thumbratio(self):
        for i in self.contents:
            ratio = image_ratio(VideoContent(i['id']).thumb_path('mobile'))
            i['ratio'] = ratio

        return self.contents
