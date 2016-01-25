import psycopg2


def condb():
    con = psycopg2.connect("dbname='newapp' user='ec2-user' host='localhost' password='8326022'")
    return con


class User:
    def __init__(self, dbid):
        self.dbid = dbid

    def get_feeds(self):
        con = condb()
        cur = con.cursor()
        cur.execute("SELECT id, thumbnail_ratio FROM myapp_content;")
        dbtuple = cur.fetchall()
        con.close()
        return dbtuple





