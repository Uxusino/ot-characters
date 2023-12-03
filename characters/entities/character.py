# The class to represent a character.
#   char_id: id as in the database
#   story_id: id of the story
#   stats: dictionary that includes the keys:
#       name: character's name
#       gender: 0=female, 1=male, 2=unknown
#       birthday: text dd/mm/YY
#       age: character's age
#       height: integer cm
#       weight: integer kg
#       appearance: string that describes character's appearance
#       personality: string that describes character's personality
#       history: string that describes character's history
#       picture: name of the picture, pictures are stored in characters/lib/avatars
#       trivia: additional information on the character
#   None of the stats are obligatory, but the character cannot be completely empty.
from services.story_service import story_service


class Character:
    def __init__(self, char_id: int, story_id: int, stats: dict) -> None:
        self.char_id = char_id
        self.story_id = story_id
        self.stats = stats

    def get_id(self) -> int:
        return self.char_id

    def get_story_id(self) -> int:
        return self.story_id

    def name(self) -> str:
        return self.stats["name"]

    def image(self) -> str:
        pic = self.stats["picture"]
        if not pic:
            pic = "default"
        return f"../library/avatars/{pic}.png"

    def gender(self) -> str:
        return {
            "0": "Female",
            "1": "Male",
            "2": "Unknown"
        }[str(self.stats["gender"])]

    def age(self) -> str:
        age = self.stats["age"]
        if age:
            return str(age)
        return "???"

    def birthday(self) -> str:
        birthday = self.stats["birthday"]
        if birthday == "??/??/????" or not birthday:
            return "Unknown"
        if birthday[-4:] == "????":
            return birthday[:-5]
        return birthday

    def height(self) -> str:
        h = self.stats["height"]
        if h:
            return f"{h} cm"
        return "??? cm"

    def weight(self) -> str:
        w = self.stats["weight"]
        if w:
            return f"{w} kg"
        return "?? kg"

    def __str__(self) -> str:
        return f"{self.stats['name']} from {story_service.get_name_by_id(self.story_id)}"

    def __eq__(self, __value: "Character") -> bool:
        return (
            self.char_id == __value.char_id
            and self.story_id == __value.story_id
            and self.stats == __value.stats
        )
