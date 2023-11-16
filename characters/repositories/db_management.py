import sqlite3
from db_connection import get_db_connection
from entities.story import Story

# Class for managing database
class Database:
    def __init__(self, con: sqlite3.Connection) -> None:
        self._con = con

    def create_story(self, name, desc=None):
        data = (name, desc)
        sql = "INSERT INTO Stories(name, desc) VALUES(?, ?)"

        cur = self._con.cursor()
        cur.execute(sql, data)
        self._con.commit()

    def delete_story(self, id):
        sql = "DELETE FROM Stories WHERE story_id=?"
        
        cur = self._con.cursor()
        cur.execute(sql, id)
        self._con.commit()

    def update_story_name(self, id, new_name):
        data = (new_name, id)
        sql = "UPDATE Stories SET name=? WHERE story_id=?"

        cur = self._con.cursor()
        cur.execute(sql, data)
        self._con.commit()

    # Returns a list of Story objects.
    def get_stories(self):
        sql = "SELECT * FROM Stories"

        cur = self._con.cursor()
        res = cur.execute(sql).fetchall()
        stories = []
        for s in res:
            story = Story(id=s[0], name=s[1], desc=s[2])
            stories.append(story)
        return stories

db = Database(get_db_connection())