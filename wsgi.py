import simplejson as json
import psycopg2

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
        dbtuple = user_db() 
        dbjson = json.dumps([{"id":str(i[0]), "ratio": i[1], "title": i[2], "name": i[3]} for i in dbtuple])
        return dbjson.encode('utf-8')
    elif first_uri == "content":
        content_id = uri_parse[2]
        dbtuple = content_db(content_id)
        dbjson = json.dumps({"title": dbtuple[0][0], "name": dbtuple[0][1]})
        return dbjson.encode('utf-8')
    else:
        return "what do you want?".encode('utf-8')

def dbcon():
    con = psycopg2.connect("dbname='newapp' password='8326022' user='ec2-user' host='localhost'")
    return con
            
def user_db():
    con = dbcon()
    cur = con.cursor()
    cur.execute("SELECT myapp_content.id,thumbnail_ratio,title,name FROM myapp_content,myapp_creator WHERE myapp_content.creator_id=myapp_creator.id;")
    dbtuple = cur.fetchall()
    con.close()
    return dbtuple    

def content_db(content_id):
    con = dbcon()
    cur = con.cursor()
    cur.execute("SELECT title, name FROM myapp_content,myapp_creator WHERE myapp_content.id={} and myapp_content.creator_id=myapp_creator.id".format(content_id))
    dbtuple = cur.fetchall()
    con.close()
    return dbtuple
