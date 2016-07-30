import simplejson as json

from ibuydeal.Content.media import image_path, image_ratio
from ibuydeal.DB.database import dictcursor
from ibuydeal.Product.item import Item


class VideoContent:
    def __init__(self, videoid):
        self.id = videoid

    def sort_time(self):
        times = self.__get_itemtimes()
        times.sort(key=lambda x: int(x['display_time'].split('-')[0]))
        timeline = self.__timeline(times)
        items = []
        for i in times:
            items.append([Item(j).basic_info for j in i['items']])

        item_time = {'items': items, 'timeline': timeline}
        return item_time

    def __get_itemtimes(self):
        with dictcursor() as cur:
            cur.execute(
                "SELECT display_time,ARRAY_AGG(item_id) as items FROM content_item,contenttime_item WHERE content_id=%s and content_item.id=contenttime_item.contenttime_id GROUP BY content_item.id",
                (self.id,))
            dbtuple = cur.fetchall()
        return dbtuple

    def __timeline(self, dbdata):
        splitdata = [i['display_time'].split('-') for i in dbdata]
        timeline = []
        [timeline.extend(i) for i in splitdata]
        int_timeline = [int(i) for i in timeline]
        return int_timeline

    def thumb_path(self, platform):
        return image_path + 'video_thumbnail/' + platform + '/' + str(self.id)

    def get_info(self):
        with dictcursor() as cur:
            cur.execute(
                "SELECT content.id,title,name FROM content,creator WHERE content.creator_id=creator_id and content.id=%s;",
                (self.id,))
            dbtuple = cur.fetchall()

    def response(self, a):
        if a == "items":
            item_time = self.sort_time()
            json_item = json.dumps(item_time)
            return json_item.encode('utf-8')


class ContentList:
    # input dictionary {content_id:order index}
    def __init__(self, ordered_content_dict):
        self._contents_order = ordered_content_dict

    @property
    def db_info(self):
        contents_list = tuple(self._contents_order.keys())
        with dictcursor() as cur:
            cur.execute(
                "SELECT content.id,title,name FROM content,creator WHERE content.creator_id=creator.id and content.id IN %s;",
                (contents_list,)
            )
            dbtuple = cur.fetchall()
        return dbtuple

    def ordered_info(self):
        temp = self.db_info
        temp.sort(key=self.__feed_order)
        return temp

    def __feed_order(self, value):
        return self._contents_order[value["id"]]

    @property
    def info(self):
        ordered_data = self.ordered_info()
        full_data = self.__add_thumb_ratio(ordered_data)
        return full_data

    def __add_thumb_ratio(self, info_list):
        for i in info_list:
            ratio = image_ratio(VideoContent(i['id']).thumb_path('mobile'))
            i['ratio'] = ratio
        return info_list
