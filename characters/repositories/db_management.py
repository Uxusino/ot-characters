import sqlite3
from db_connection import get_db_connection

# Class for managing database
class Database:
    def __init__(self, con: sqlite3.Connection) -> None:
        self._con = con

    # Returns the id of the story
    def create_story(self, name, desc=None) -> int:
        data = (name, desc)
        sql = "INSERT INTO Stories(name, desc) VALUES(?, ?)"

        cur = self._con.cursor()
        cur.execute(sql, data)
        story_id = cur.lastrowid
        self._con.commit()
        return story_id

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

    # Returns a list of dictionaries as:
    # {
    #   "id": story.id,
    #   "name": story.name,
    #   "desc": story.desc
    # }
    def get_stories(self) -> list[dict]:
        sql = "SELECT * FROM Stories"

        cur = self._con.cursor()
        res = cur.execute(sql).fetchall()
        stories = []
        for s in res:
            story = {
                "id": s[0],
                "name":s[1],
                "desc": s[2]
            }   
            stories.append(story)
        return stories
    
    def count_stories(self) -> int:
        sql = "SELECT COUNT(*) FROM Stories"
        cur = self._con.cursor()
        res = cur.execute(sql).fetchone()
        return res[0]
    
    # Deletes all stories.
    def clear_stories(self) -> None:
        sql = "DELETE FROM Stories"
        cur = self._con.cursor()
        cur.execute(sql)
        self._con.commit()

db = Database(get_db_connection())