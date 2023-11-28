from initialize_db import initialize_database
from services.character_service import char_service, Character
from services.story_service import story_service, Story
import unittest
import os
import sys

dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(dir)
sys.path.append(root_dir)


class TestCharacterService(unittest.TestCase):
    def setUp(self):
        initialize_database()

        self.dummy_story = story_service.create_story(name="Dummy Story")

        self.dummy_character = Character(
            char_id=1,
            story_id=1,
            stats={
                "name": "Dummy",
                "gender": 2,
                "birthday": "24/12/1999",
                "age": 23,
                "height": 170,
                "weight": 60,
                "appearance": "",
                "personality": "",
                "history": "",
                "picture": None,
                "trivia": ""
            }
        )

    def test_create_character(self):
        testcharacter = char_service.create_character(
            (
                "Dummy",
                "Unknown",
                ("24", "12", "1999"),
                "23",
                "170",
                "60",
                "",
                "",
                "",
                None,
                ""
            ),
            1
        )

        self.assertEqual(testcharacter, self.dummy_character)

    def test_returns_right_list(self):
        testcharacter = char_service.create_character(
            (
                "Dummy",
                "Unknown",
                ("24", "12", "1999"),
                "23",
                "170",
                "60",
                "",
                "",
                "",
                None,
                ""
            ),
            1
        )

        charlist = char_service.get_characters_by_story_id(1)
        self.assertEqual(charlist, [self.dummy_character])
