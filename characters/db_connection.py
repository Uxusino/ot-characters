import sqlite3
from config import DB_PATH #pylint: disable=E0401

con = sqlite3.connect(DB_PATH)
con.row_factory = sqlite3.Row

def get_db_connection():
    return con
