
from contextlib import closing
import sqlite3

userdateSchema = 'userdateSchema.sql'
userdateSite = 'userdate.db'
def connect_userdb():
    return sqlite3.connect(userdateSite)

def init_userdb():
    with closing(connect_userdb()) as db:
        with open(userdateSchema,"r") as f:
            db.cursor().executescript(f.read())
        db.commit()

try:
    open(userdateSite,"r")
except Exception,e:
    init_userdb()
