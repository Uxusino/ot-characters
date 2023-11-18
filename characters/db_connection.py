import os
import sqlite3
from config import DB_PATH

database = "db.sqlite"

con = sqlite3.connect(DB_PATH)
con.row_factory = sqlite3.Row

def get_db_connection():
    return con
