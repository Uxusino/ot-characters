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
                "birthday": "24/12/????",
                "age": 23,
                "height": 170,
                "weight": 60,
                "appearance": None,
                "personality": None,
                "history": None,
                "picture": None,
                "trivia": None
            }
        )

        self.dummy_character_stats = (
            "Dummy",
            "Unknown",
            ("24", "12", None),
            "23",
            "170",
            "60",
            "",
            "",
            "",
            None,
            ""
        )

    def test_create_character(self):
        testcharacter = char_service.create_character(
            self.dummy_character_stats, 1)

        self.assertEqual(testcharacter, self.dummy_character)

    def test_returns_right_list(self):
        char_service.create_character(self.dummy_character_stats, 1)

        charlist = char_service.get_characters_by_story_id(1)
        self.assertEqual(charlist, [self.dummy_character])

    def test_clear_stories_clears_characters(self):
        char_service.create_character(self.dummy_character_stats, 1)
        story_service.clear_stories(test=True)
        chars = char_service.get_characters_by_story_id(1)

        self.assertEqual(chars, None)

    def test_get_character_relations(self):
        char1 = char_service.create_character(self.dummy_character_stats, 1)
        char2 = char_service.create_character(self.dummy_character_stats, 1)
        char_service.set_relations(
            char1=char1, char2=char2, relation="sibling", former=0)
        relations = char_service.get_character_relations(character=char1)

        self.assertEqual(relations, [("Dummy", 0, "sibling", 2, 5, 1, 5)])

    def test_clear_stories_clears_relations(self):
        char1 = char_service.create_character(self.dummy_character_stats, 1)
        char2 = char_service.create_character(self.dummy_character_stats, 1)
        char_service.set_relations(
            char1=char1, char2=char2, relation="sibling", former=0)
        story_service.clear_stories(test=True)
        story_service.create_story("Dummy Story 2")
        char3 = char_service.create_character(self.dummy_character_stats, 1)
        relations = char_service.get_character_relations(character=char3)

        self.assertEqual(relations, None)

    def test_update_character(self):
        char = char_service.create_character(self.dummy_character_stats, 1)
        stats = ("f", "22/12/2023", "", "170", "", "bald head blue eyes", "", "", "", "Dummella", char)
        edited = Character(
            char_id=1,
            story_id=1,
            stats={
                "name": "Dummella",
                "gender": 0,
                "birthday": "22/12/2023",
                "age": None,
                "height": 170,
                "weight": None,
                "appearance": "bald head blue eyes",
                "personality": None,
                "history": None,
                "picture": None,
                "trivia": None
            }
        )
        char_service.update_character(stats=stats)
        new_dummy = char_service.get_characters_by_story_id(1)[0]
        print(new_dummy)
        print(edited)

        self.assertEqual(new_dummy, edited)

    def test_delete_twosided_relation(self):
        char1 = char_service.create_character(self.dummy_character_stats, 1)
        char2 = char_service.create_character(self.dummy_character_stats, 1)
        char_service.set_relations(char1=char1, char2=char2, relation="parent", former=0)
        char_service.delete_relation(char1_id=char2.char_id, char2_id=char1.char_id, rel_id=2, two_sided=1, counterpart=1)
        res = char_service.get_character_relations(char1)

        self.assertEqual(res, None)

    def test_delete_single_story_deletes_relations(self):
        char1 = char_service.create_character(self.dummy_character_stats, 1)
        char2 = char_service.create_character(self.dummy_character_stats, 1)
        char_service.set_relations(char1=char1, char2=char2, relation="parent", former=0)
        story_service.delete_story(1)
        story = story_service.create_story(name="Dummy Story")
        char3 = char_service.create_character(self.dummy_character_stats, story_id=story.story_id)
        char_service.create_character(self.dummy_character_stats, story_id=story.story_id)
        res = char_service.get_character_relations(char3)

        self.assertEqual(res, None)

    def test_format_character_stats(self):
        char = char_service.create_character(self.dummy_character_stats, 1)
        age = char.age()
        bday = char.birthday()
        height = char.height()
        weight = char.weight()

        self.assertEqual(age, "23")
        self.assertEqual(bday, "24/12")
        self.assertEqual(height, "170 cm")
        self.assertEqual(weight, "60 kg")