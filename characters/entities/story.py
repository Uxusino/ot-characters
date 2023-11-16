# This class represents a story.
#   id:     id as in the database
#   name:   Name of the story
#   desc:   Description, is not obligatory, default None

class Story:
    def __init__(self, id: int, name: str, desc: str = None) -> None:
        self.id = id
        self.name = name
        self.desc = desc