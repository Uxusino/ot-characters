from initialize_db import initialize_database
from services.story_service import story_service, Story
import unittest
import os
import sys

dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(dir)
sys.path.append(root_dir)


class TestStoryService(unittest.TestCase):
    def setUp(self):
        initialize_database()

        self.storyname = "Dummy Story"
        self.storydesc = "Dummy Description"
        self.long_storyname = "Exiled in a Class Trial for “Poor Dexterity”. Because He Was Dexterous, He Lived on His Own. Because of His Dexterity, He Was Able to Use All the Skills and Magic of the Higher Ranks, Making Him Invincible. I Decided to Live on My Own, but the People Around Me Wouldn’t Leave Me Alone."

        self.story = Story(story_id=1, name=self.storyname,
                           desc=self.storydesc)
        self.story_no_desc = Story(story_id=1, name=self.storyname, desc=None)

    # Must return a Story object if everything's correct,
    # None if input is invalid
    def test_create_story(self):
        teststory = story_service.create_story(
            name=self.storyname, desc=self.storydesc)

        self.assertEqual(str(teststory), str(self.story))

    def test_create_story_without_desc(self):
        teststory = story_service.create_story(name=self.storyname, desc=None)

        self.assertEqual(str(teststory), str(self.story_no_desc))

    def test_count(self):
        story_service.create_story(name=self.storyname, desc=self.storydesc)
        count = story_service.count_stories()

        self.assertEqual(count, 1)

    # All cases must return None and the database must be empty
    def test_create_story_invalid(self):
        teststory_long = story_service.create_story(
            name=self.long_storyname, desc=self.storydesc)
        teststory_empty = story_service.create_story(
            name=None, desc=self.storydesc)
        count = story_service.count_stories()

        self.assertEqual(teststory_long, None)
        self.assertEqual(teststory_empty, None)
        self.assertEqual(count, 0)

    def test_get_stories(self):
        story_service.create_story(name=self.storyname, desc=self.storydesc)
        story_service.create_story(name=self.storydesc, desc=self.storyname)
        stories = story_service.get_stories()
        model = [
            Story(story_id=1, name=self.storyname, desc=self.storydesc),
            Story(story_id=2, name=self.storydesc, desc=self.storyname)
        ]

        self.assertEqual(stories, model)
