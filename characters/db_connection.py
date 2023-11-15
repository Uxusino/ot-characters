import sqlite3

con = sqlite3.connect("db.db")
con.row_factory = sqlite3.Row

def get_db_connection():
    return con
