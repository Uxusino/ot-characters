import sqlite3


def execute_sql(con: sqlite3.Connection, sql: str, data: tuple = None) -> sqlite3.Cursor:
    """Executes SQL query and returns Cursor object.

    Args:
        con (sqlite3.Connection): Connection to SQLite database.
        sql (str): SQL string to be executed.
        data (tuple, optional): Tuple with data to be used in SQL query. Defaults to None.

    Returns:
        sqlite3.Cursor: Cursor object to retrieve further information.
    """

    cur = con.cursor()
    if not data:
        cur.execute(sql)
    else:
        cur.execute(sql, data)
    con.commit()
    return cur
