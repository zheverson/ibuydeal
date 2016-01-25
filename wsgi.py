import model
import simplejson as json

def app(environ, start_response):
    body = response(environ)
    start_response("200 ok", [("Content-type", "application/json")])
    return [body]


def response(environ):
    method = environ['REQUEST_METHOD']
    uri = environ['RAW_URI']
    uri_parse = uri.split('/')
    first_uri = uri_parse[1]
    if first_uri == "user":
        user = model.User()
        dbtuple = user.get_feeds()
        dbjson = json.dumps([{"id": i[0], "ratio": i[1]} for i in dbtuple])
        return dbjson.encode('utf-8')
    else:
        return "what do you want?".encode('utf-8')


