from repositories.db_management import db
from entities.story import Story

# This class is a step between database and Story as an object,
# since using the both in UI class looks like a mess.
# This class will also be responsible for checking if user's input
# is valid or not.
class StoryService:
    def __init__(self) -> None:
        pass
    
    # Gets list of dictionaries from database and return list of Stories
    def get_stories(self) -> list[Story]:
        stories_dict = db.get_stories()
        stories = []
        for s in stories_dict:
            story = Story(
                id=s['id'],
                name=s['name'],
                desc=s['desc']
            )
            stories.append(story)
        return stories
    
    def count_stories(self) -> int:
        return db.count_stories()
    
    # Creates a story and return a Story object.
    # If input is invalid, returns None.
    def create_story(self, name: str, desc=None) -> Story:
        if len(name) > 100:
            return None
        if desc and len(desc) > 500:
            return None
        story_id = db.create_story(name=name, desc=desc)
        story = Story(id=story_id, name=name, desc=desc)
        return story
    
    def clear_stories(self):
        db.clear_stories()
    
story_service = StoryService()