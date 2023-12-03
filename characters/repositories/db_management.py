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

    def create_character(self, stats: tuple) -> int:
        data = stats
        sql = """
            INSERT INTO Characters(
                story_id,
                name,
                gender,
                birthday,
                age,
                height,
                weight,
                appearance,
                personality,
                history,
                picture,
                trivia
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cur = self._con.cursor()
        cur.execute(sql, data)
        char_id = cur.lastrowid
        self._con.commit()
        print(
            f"Succesfully inserted character with id {char_id} into database.")
        return char_id

    def delete_story(self, story_id):
        sql = "DELETE FROM Stories WHERE story_id=?"
        cur = self._con.cursor()
        cur.execute(sql, story_id)
        self._con.commit()

    def update_story_name(self, story_id, new_name):
        data = (new_name, story_id)
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
                "name": s[1],
                "desc": s[2]
            }
            stories.append(story)
        return stories

    def get_story_by_id(self, story_id: int) -> dict:
        sql = "SELECT * FROM Stories WHERE story_id=?"

        cur = self._con.cursor()
        res = cur.execute(sql, (story_id, )).fetchone()
        story = {
            "id": res[0],
            "name": res[1],
            "desc": res[2]
        }
        return story

    def get_characters_by_story_id(self, story_id: int) -> list[dict]:
        sql = "SELECT * FROM Characters WHERE story_id=?"

        cur = self._con.cursor()
        res = cur.execute(sql, (story_id, )).fetchall()
        if not res:
            return None
        characters = []
        for c in res:
            character = {
                "char_id": c[0],
                "story_id": c[1],
                "stats": {
                    "name": c[2],
                    "gender": c[3],
                    "birthday": c[4],
                    "age": c[5],
                    "height": c[6],
                    "weight": c[7],
                    "appearance": c[8],
                    "personality": c[9],
                    "history": c[10],
                    "picture": c[11],
                    "trivia": c[12]
                }
            }
            characters.append(character)
        return characters

    def get_name_by_id(self, story_id) -> str:
        sql = "SELECT name FROM Stories WHERE story_id=?"

        cur = self._con.cursor()
        res = cur.execute(sql, (story_id,)).fetchone()[0]
        return res

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

    def clear_characters(self) -> None:
        sql = "DELETE FROM Characters"
        cur = self._con.cursor()
        cur.execute(sql)
        self._con.commit()


db = Database(get_db_connection())
