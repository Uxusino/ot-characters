# This class represents a story.
#   id:     id as in the database
#   name:   Name of the story
#   desc:   Description, is not obligatory, default None

class Story:
    def __init__(self, story_id: int, name: str, desc: str = None) -> None:
        self.story_id = story_id
        self.name = name
        self.desc = desc

    def get_id(self):
        return self.story_id
    
    def get_name(self):
        return self.name
    
    def get_desc(self):
        return self.desc

    def __str__(self) -> str:
        return f"{self.story_id}. {self.name}: {self.desc}"

    def __eq__(self, __value: "Story") -> bool:
        return (
            self.story_id == __value.story_id
            and self.name == __value.name
            and self.desc == __value.desc
        )
