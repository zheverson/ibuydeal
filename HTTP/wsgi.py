from Product.item import Item
from content import VideoContent
from user import User


# wsgi interface function
def app(environ, start_response):
    body = response(environ)
    start_response("200 ok", [("Content-type", "application/json")])
    return [body]


#  environ is a dict, take this dict as input, which include uri, method, parameters, and return response
def response(environ):
    method = environ['REQUEST_METHOD']
    uri = environ['RAW_URI']

    # uri_parse is www.111.com/1st/2nd/3rd split by /
    uri_parse = uri.split('/')

    # 1st in uri_parse
    first_uri = uri_parse[1]

    if first_uri == "user":
        user = User()
        return user.response()
    elif first_uri == "content":
        if uri_parse[2] == "video":
            content_id = int(uri_parse[3])
            content = VideoContent(content_id)
            return content.response(uri_parse[4])
    elif first_uri == "item":
        item_id = int(uri_parse[2])
        item = Item(item_id)
        return item.response(uri_parse[3])
    else:
        return "what do you want?".encode('utf-8')


