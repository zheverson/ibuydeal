import psycopg2
import psycopg2.extras
import simplejson as json

con = psycopg2.connect("dbname='newapp' password='8326022' user='ec2-user' host='localhost'")


def dictcursor():
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return cur


def cursor():
    return con.cursor()


def json_response(data):
    return json.dumps(data).encode('utf-8')
