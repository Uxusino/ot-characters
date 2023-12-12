"""Stepping stone between database and Story as an object.

This class is also responsible for checking whether user's input is valid or not.

    Returns:
        StoryService: Controls everything to do with stories.
"""

from repositories.db_management import db
from repositories.file_management import rep
from entities.story import Story


class StoryService:
    def __init__(self) -> None:
        pass

    def get_stories(self) -> list[Story]:
        """Obtains a list of dictionaries from database and return a list of Stories

        Returns:
            list[Story]: Contains all of user's stories.
        """

        stories_dict = db.get_stories()
        stories = []
        for s in stories_dict:
            story = Story(
                story_id=s['id'],
                name=s['name'],
                desc=s['desc']
            )
            stories.append(story)
        return stories

    def get_story_by_id(self, story_id: int) -> Story:
        """Searches a story by story id.

        Args:
            story_id (int): Story id.

        Returns:
            Story: Story object for the corresponding story.
        """

        story_dict = db.get_story_by_id(story_id=story_id)
        return Story(story_id=story_dict["id"], name=story_dict["name"], desc=story_dict["desc"])

    def count_stories(self) -> int:
        """Counts total stories of a user.

        Returns:
            int: Total number of stories.
        """
        return db.count_stories()

    def create_story(self, name: str, desc=None) -> Story:
        """Creates a story and return a Story object.

        Args:
            name (str): Story name
            desc (_type_, optional): Story description. Defaults to None.

        Returns:
            Story: Story object for a new created story.
            None: Returns None if input is invalid.
        """
        if not name:
            return None
        if len(name) > 100:
            return None
        if desc and len(desc) > 500:
            return None
        story_id = db.create_story(name=name, desc=desc)
        story = Story(story_id=story_id, name=name, desc=desc)
        return story

    def clear_stories(self):
        """Deletes all stories and characters.
        """
        db.clear_stories()
        db.clear_characters()
        rep.delete_all_avatars()

    def delete_story(self, story_id: int):
        """Deletes a story based on its id.

        Args:
            story_id (int): Story id to be deleted.
        """
        db.delete_story(story_id=story_id)

    def get_name_by_id(self, story_id: int) -> str:
        """Obtains story name by its id.

        Args:
            story_id (int): Story id.

        Returns:
            str: Story name.
        """
        return db.get_name_by_id(story_id=story_id)

    def get_mean_age(self, story_id: int) -> float:
        """Calculates mean age of characters in a story.

        Args:
            story_id (int): Story id.

        Returns:
            float: Mean age of characters of the story.
        """
        return db.mean_age(story_id=story_id)

story_service = StoryService()
