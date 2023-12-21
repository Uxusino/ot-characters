"""Class for controlling the database. Contains methods for managing characters.

    Returns:
        Database: A Database object.
"""

import sqlite3
from db_connection import get_db_connection
from services.formatter import formatter
from . import executor as e


class CharactersDatabase:
    def __init__(self, con: sqlite3.Connection) -> None:
        self._con = con

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

        cur = e.execute_sql(self._con, sql, data)
        char_id = cur.lastrowid
        return char_id

    def update_character(self, stats: tuple) -> None:
        """Updates character's information in the database.

        Args:
            stats (tuple): Information to be updated
        """

        sql = """
            UPDATE Characters
            SET
                gender=?,
                birthday=?,
                age=?,
                height=?,
                weight=?,
                appearance=?,
                personality=?,
                history=?,
                trivia=?,
                name=?
            WHERE char_id=?
        """
        e.execute_sql(self._con, sql, stats)

    def update_image(self, picture: str, char_id: int) -> None:
        """Updated character's avatar.

        Args:
            picture (str): Name of the new avatar
            char_id (int): Character id
        """

        sql = "UPDATE Characters SET picture=? WHERE char_id=?"
        e.execute_sql(self._con, sql, (picture, char_id))

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
        characters = formatter.characters_to_dict(res)
        return characters

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

    def get_character_relations(self, char_id: int) -> list[tuple]:
        """All relationships of a certain character.

        Args:
            char_id (int): Character id

        Returns:
            list[tuple]: (name, former, relation, char2_id, relation id, two-sided, counterpart)
        """

        sql = """
            SELECT char.name, charrel.former,
                CASE
                    WHEN char.gender = 0 THEN rel.female_name
                    WHEN char.gender = 1 THEN rel.male_name
                    ELSE rel.name
                END AS relation_name,
                charrel.char2_id, rel.relation_id, rel.two_sided,
                CASE
                    WHEN rel.two_sided = 1 THEN rel.counterpart
                    ELSE NULL
                END AS counterpart
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
            relations.append((r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
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

        e.execute_sql(self._con, sql, data)

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

    def delete_character(self, char_id: int) -> None:
        """Deletes a character by their id.

        Args:
            char_id (int): Character id
        """

        sql = "DELETE FROM Characters WHERE char_id=?"
        e.execute_sql(self._con, sql, (char_id,))

    def delete_character_relations(self, char_id: int) -> None:
        """Deletes all relationships of a character.

        Args:
            char_id (int): Character id
        """

        sql = "DELETE FROM CharacterRelations WHERE char1_id=? OR char2_id=?"
        e.execute_sql(self._con, sql, (char_id, char_id))

    def delete_relation(self, char1_id: int, char2_id: int, rel_id: int,
                        two_sided: bool, counterpart: int = None) -> None:
        """Deletes a relationship between two characters.

        Args:
            char1_id (int): Id of the first character
            char2_id (int): Id of the second character
            rel_id (int): Relation id
            two_sided (bool): True if two-sided, False if not
            counterpart (int): Id of respective relation, if two-sided
        """

        data = (char1_id, char2_id, rel_id)
        sql = """
            DELETE FROM CharacterRelations
            WHERE char1_id=? AND char2_id=? AND relation_id=?
        """
        e.execute_sql(self._con, sql, data)

        if two_sided:
            data2 = (char2_id, char1_id, counterpart)
            e.execute_sql(self._con, sql, data2)

    def clear_characters(self) -> None:
        """Deletes all characters.
        """

        sql = "DELETE FROM Characters"
        e.execute_sql(self._con, sql)

    def clear_relations(self) -> None:
        """Deletes all relations.
        """

        sql = "DELETE FROM CharacterRelations"
        e.execute_sql(self._con, sql)


char_db = CharactersDatabase(get_db_connection())
