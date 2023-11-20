import sqlite3
import json
import os
from db_connection import get_db_connection

def drop_tables(con: sqlite3.Connection):
    cur = con.cursor()
    tables = ["Stories", "Characters", "Relations", "CharacterRelations"]
    for table in tables:
        cur.execute(f"DROP TABLE IF EXISTS {table}")
    con.commit()

def create_tables(con: sqlite3.Connection):
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE Stories (
            story_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            desc TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE Characters (
            char_id INTEGER PRIMARY KEY,
            story_id INTEGER,
            name TEXT NOT NULL,
            gender INTEGER,
            birthday TEXT,
            age INTEGER,
            height INTEGER,
            weight INTEGER,
            appearance TEXT,
            personality TEXT,
            history TEXT,
            picture TEXT,
            trivia TEXT,
            FOREIGN KEY (story_id)
                REFERENCES Stories(story_id)
                    ON DELETE CASCADE
        )
    """)
    cur.execute("""
        CREATE TABLE Relations (
            relation_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            female_name TEXT,
            male_name TEXT,
            two_sided INTEGER NOT NULL,
            counterpart INTEGER DEFAULT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE CharacterRelations (
            char1_id INTEGER NOT NULL,
            char2_id INTEGER NOT NULL,
            relation_id INTEGER NOT NULL,
            former INTEGER DEFAULT 0,
            FOREIGN KEY (char1_id)
                REFERENCES Characters(char_id)
                    ON DELETE CASCADE,
            FOREIGN KEY (char2_id)
                REFERENCES Characters(char_id)
                    ON DELETE CASCADE,
            FOREIGN KEY (relation_id)
                REFERENCES Relations(relation_id)
                    ON DELETE CASCADE
        )
    """)
    con.commit()

# Loads json into database for easier handling and code reading
def load_relations(con: sqlite3.Connection):
    fpath = os.path.abspath(__file__)
    rpath = os.path.join(os.path.dirname(fpath), "data", "relations.json")
    with open(rpath) as f:
        raw_relations = f.read()
        relations = json.loads(raw_relations)
    relations_list = relations['relations']
    sql_inputs = []
    for r in relations_list:
        if r['two_sided'] == 1:
            i = (r['id'], r['name'], r['female_name'], r['male_name'], r['two_sided'], r['counterpart'])
        else:
            i = (r['id'], r['name'], r['female_name'], r['male_name'], r['two_sided'], None)
        sql_inputs.append(i)

    sql = "INSERT INTO Relations ( relation_id, name, female_name, male_name, two_sided, counterpart ) VALUES (?, ?, ?, ?, ?, ?)"

    cur = con.cursor()
    try:
        cur.executemany(sql, sql_inputs)
        con.commit()
        print("Succesfully added relations to the table.")
    except Exception as e:
        con.rollback()
        print("Something went horribly wrong :(" + str(e))


# Deletes old database, creates new and loads relations
def initialize_database():
    con = get_db_connection()
    drop_tables(con)
    create_tables(con)
    load_relations(con)
    print("Succesfully initialized database.")

if __name__ == "__main__":
    initialize_database()