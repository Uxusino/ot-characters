"""Class for controlling the database. Contains methods for managing stories.

    Returns:
        Database: A Database object.
"""

import sqlite3
from db_connection import get_db_connection
from . import executor as e


class StoriesDatabase:
    def __init__(self, con: sqlite3.Connection) -> None:
        self._con = con

    def create_story(self, name: str, desc: str = None) -> int:
        """Creates a story and adds it to the database.

        Args:
            name (str): Name of the story.
            desc (str, optional): Description of the story. Defaults to None.

        Returns:
            int: New story's id as in the database.
        """

        data = (name, desc)
        sql = "INSERT INTO Stories(name, desc) VALUES(?, ?)"

        cur = e.execute_sql(self._con, sql, data)
        story_id = cur.lastrowid
        return story_id

    def delete_story(self, story_id: int) -> None:
        """Deletes story from the database.

        Args:
            story_id (int): Story id
        """

        sql = "DELETE FROM Stories WHERE story_id=?"
        e.execute_sql(self._con, sql, (story_id,))

    def delete_characters_of_a_story(self, story_id: int) -> None:
        """Deletes all characters from a story.

        Args:
            story_id (int): Story id
        """

        sql = "DELETE FROM Characters WHERE story_id=?"
        e.execute_sql(self._con, sql, (story_id,))

    def delete_relations_of_a_story(self, story_id: int) -> None:
        """Deletes all relations of characters in a story.

        Args:
            story_id (int): Story id
        """

        sql = """
            DELETE FROM CharacterRelations
            WHERE char1_id IN (
                SELECT c.char_id
                FROM Characters c
                WHERE c.story_id = ?
            )
        """
        e.execute_sql(self._con, sql, (story_id,))

    def update_story_name(self, story_id: int, new_name: str) -> None:
        """Updates story's name based on its id.

        Args:
            story_id (int): Story id
            new_name (str): New name
        """

        data = (new_name, story_id)
        sql = "UPDATE Stories SET name=? WHERE story_id=?"

        e.execute_sql(self._con, sql, data)

    def update_story_desc(self, story_id: int, new_desc: str) -> None:
        """Updates story's description based on its id.

        Args:
            story_id (int): Story id
            new_desc (str): New description
        """

        data = (new_desc, story_id)
        sql = "UPDATE Stories SET desc=? WHERE story_id=?"

        e.execute_sql(self._con, sql, data)

    def get_stories(self) -> list[dict]:
        """Returns all stories as a list of dictionaries.

        {
            "id": story.id,
            "name": story.name,
            "desc": story.desc
        }

        Returns:
            list[dict]: List that contains dictionaries, each of them represents a single story.
        """
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
        """Obtains all information about a story by its id.

        {
            "id": story.id,
            "name": story.name,
            "desc": story.desc
        }

        Args:
            story_id (int): Story's id as in the database.

        Returns:
            dict: Has all information about a story.
        """
        sql = "SELECT * FROM Stories WHERE story_id=?"

        cur = self._con.cursor()
        res = cur.execute(sql, (story_id, )).fetchone()
        story = {
            "id": res[0],
            "name": res[1],
            "desc": res[2]
        }
        return story

    def get_all_avatars_of_a_story(self, story_id: int) -> list[str]:
        """Obtains all avatar names of characters in a story.

        Args:
            story_id (int): Story id

        Returns:
            list[str]: List of avatar names
        """

        sql = "SELECT picture FROM Characters WHERE story_id = ? AND picture IS NOT NULL"

        cur = self._con.cursor()
        res = cur.execute(sql, (story_id,)).fetchall()
        avatars = []
        for a in res:
            avatars.append(a[0])
        return avatars

    def get_name_by_id(self, story_id: int) -> str:
        """Searches name of a story based on its id.

        Args:
            story_id (int): Story id as in the database.

        Returns:
            str: Name of the story.
        """

        sql = "SELECT name FROM Stories WHERE story_id=?"

        cur = self._con.cursor()
        res = cur.execute(sql, (story_id,)).fetchone()[0]
        return res

    def count_stories(self) -> int:
        """Counts total stories.

        Returns:
            int: Total number of stories.
        """

        sql = "SELECT COUNT(*) FROM Stories"
        cur = self._con.cursor()
        res = cur.execute(sql).fetchone()
        return res[0]

    def mean_age(self, story_id: int) -> float:
        """Calculates mean age of characters in a story.

        Args:
            story_id (int): Story id.

        Returns:
            float: Mean age of characters of the story.
        """

        sql = """
            SELECT COALESCE(SUM(c.age) / NULLIF(CAST(COUNT(c.age) AS FLOAT), 0), 0)
            FROM Stories s
            JOIN Characters c ON c.story_id=s.story_id AND c.age IS NOT NULL
            WHERE s.story_id = ?
        """

        cur = self._con.cursor()
        res = cur.execute(sql, (story_id,)).fetchone()[0]
        return round(res, 1)

    def clear_stories(self) -> None:
        """Deletes all stories.
        """

        sql = "DELETE FROM Stories"
        e.execute_sql(self._con, sql)


story_db = StoriesDatabase(get_db_connection())
