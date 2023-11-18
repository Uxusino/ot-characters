# This class represents a story.
#   id:     id as in the database
#   name:   Name of the story
#   desc:   Description, is not obligatory, default None

class Story:
    def __init__(self, id: int, name: str, desc: str = None) -> None:
        self.id = id
        self.name = name
        self.desc = desc

    def __str__(self) -> str:
        return f"{self.id}. {self.name}: {self.desc}"
    
    def __eq__(self, __value: "Story") -> bool:
        if self.id == __value.id and self.name == __value.name and self.desc == __value.desc:
            return True
        else:
            return False