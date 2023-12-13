"""Class for controling the database.

    Returns:
        Database: A Database object.
"""

import sqlite3
from db_connection import get_db_connection


class Database:
    def __init__(self, con: sqlite3.Connection) -> None:
        self._con = con

    def _execute(self, sql: str, data: tuple = None) -> sqlite3.Cursor:
        """Executes SQL query and returns Cursor object.

        Args:
            sql (str): SQL string to be executed.
            data (tuple, optional): Tuple with data to be used in SQL query. Defaults to None.

        Returns:
            sqlite3.Cursor: Cursor object to retrieve further information.
        """

        cur = self._con.cursor()
        if not data:
            cur.execute(sql)
        else:
            cur.execute(sql, data)
        self._con.commit()
        return cur

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

        cur = self._execute(sql, data)
        story_id = cur.lastrowid
        return story_id

    def create_character(self, stats: tuple) -> int:
        """Creates a character and adds it to the database.
        Args:
            stats (tuple): tuple that contains all character information.

        Returns:
            int: New character's id as in the database.
        """

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

        cur = self._execute(sql, data)
        char_id = cur.lastrowid
        return char_id

    def delete_story(self, story_id: int) -> None:
        """Deletes story from the database.

        Args:
            story_id (int): Story id
        """

        sql = "DELETE FROM Stories WHERE story_id=?"
        self._execute(sql)

    def update_story_name(self, story_id: int, new_name: str) -> None:
        """Updates story's name based on its id.

        Args:
            story_id (int): Story id
            new_name (str): New name
        """

        data = (new_name, story_id)
        sql = "UPDATE Stories SET name=? WHERE story_id=?"

        self._execute(sql, data)

    def update_story_desc(self, story_id: int, new_desc: str) -> None:
        """Updates story's description based on its id.

        Args:
            story_id (int): Story id
            new_desc (str): New description
        """

        data = (new_desc, story_id)
        sql = "UPDATE Stories SET desc=? WHERE story_id=?"

        self._execute(sql, data)

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

    def _characters_to_dict(self, lst: list) -> list[dict]:
        """Converts list with raw characters data into a clean dictionary.

        Args:
            lst (list): Raw list with data from the database.

        Returns:
            list[dict]: Contains characters represented by a dictionary.
        """

        characters = []
        for c in lst:
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

    def get_characters_by_story_id(self, story_id: int) -> list[dict]:
        """Searches all characters from a certain story.

        Args:
            story_id (int): Story id as in the database.

        Returns:
            list[dict]: Contains characters represented by a dictionary.
        """

        sql = "SELECT * FROM Characters WHERE story_id=?"

        cur = self._con.cursor()
        res = cur.execute(sql, (story_id, )).fetchall()
        if not res:
            return None
        characters = self._characters_to_dict(res)
        return characters

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

    def get_relations(self) -> list[str]:
        """Names of all relations from the database.

        Returns:
            list[str]: List that contains all relation names.
        """

        sql = "SELECT name FROM Relations"

        cur = self._con.cursor()
        res = cur.execute(sql).fetchall()
        relations = []
        for r in res:
            relations.append(r[0])
        return relations

    def get_relation_id_from_name(self, name: str) -> int:
        """Id of a relation based on its name.

        Args:
            name (str): Unique name of a relation.

        Returns:
            int: Relation id.
        """

        sql = "SELECT relation_id FROM Relations WHERE name=?"

        cur = self._con.cursor()
        res = cur.execute(sql, (name,)).fetchone()[0]
        return res

    def get_character_relations(self, char_id: int) -> list[tuple]:
        """All relationships of a certain character.

        Args:
            char_id (int): Character id as in the database.

        Returns:
            list[tuple]: (character's name, is relationship former, relation's name)
        """

        sql = """
            SELECT char.name, charrel.former,
                CASE
                    WHEN char.gender = 0 THEN rel.female_name
                    WHEN char.gender = 1 THEN rel.male_name
                    ELSE rel.name
                END AS relation_name
            FROM CharacterRelations charrel
            JOIN Characters char ON char.char_id = charrel.char2_id
            JOIN Relations rel ON rel.relation_id = charrel.relation_id
            WHERE charrel.char1_id = ?
        """

        cur = self._con.cursor()
        res = cur.execute(sql, (char_id,)).fetchall()
        if not res:
            return None
        relations = []
        for r in res:
            relations.append((r[0], r[1], r[2]))
        return relations

    def _is_relation_twosided(self, relation_id: int) -> tuple:
        """Checks if a relation is two-sided or not. If it is, returns also the counterpart.

        Args:
            relation_id (int): Relation id.

        Returns:
            tuple: (True, counterpart_id) if two-sided, (False, None) if not.
        """

        sql = """
            SELECT two_sided,
                CASE
                    WHEN two_sided = 1 THEN counterpart
                    ELSE NULL
                END AS counterpart
            FROM Relations
            WHERE relation_id=?
        """

        cur = self._con.cursor()
        res = cur.execute(sql, (relation_id, )).fetchone()
        return res

    def set_relation(self, char1_id: int, char2_id: int, relation_id: int, former: int) -> None:
        """Sets a relationship between two characters.

        Char2 is a ___ to char1.
        If the relation is two-sided, also updates char2.

        Args:
            char1_id (int): Id of the first character.
            char2_id (int): Id of the second character.
            relation_id (int): Relation id.
            former (int): Is the relationship former? 0 or 1
        """

        ts = self._is_relation_twosided(relation_id=relation_id)

        if ts[0] == 1:
            data = (char1_id, char2_id, relation_id, former,
                    char2_id, char1_id, ts[1], former)
            sql = """
                INSERT INTO CharacterRelations(
                    char1_id,
                    char2_id,
                    relation_id,
                    former
                ) VALUES (?, ?, ?, ?),
                (?, ?, ?, ?)
            """
        else:
            data = (char1_id, char2_id, relation_id, former)
            sql = """
                INSERT INTO CharacterRelations(
                    char1_id,
                    char2_id,
                    relation_id,
                    former
                ) VALUES (?, ?, ?, ?)
            """

        self._execute(sql, data)

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

    # Deletes all stories.
    def clear_stories(self) -> None:
        """Deletes all stories.
        """

        sql = "DELETE FROM Stories"
        self._execute(sql)

    def clear_characters(self) -> None:
        """Deletes all characters.
        """

        sql = "DELETE FROM Characters"
        self._execute(sql)

    def clear_relations(self) -> None:
        """Deletes all relations.
        """

        sql = "DELETE FROM CharacterRelations"
        self._execute(sql)


db = Database(get_db_connection())
