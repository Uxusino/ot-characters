import os
import sqlite3

dirname = os.path.abspath(__file__)

con = sqlite3.connect(os.path.join((os.path.dirname(dirname)), "data", "db.db"))
con.row_factory = sqlite3.Row

def get_db_connection():
    return con
