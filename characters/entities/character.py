"""The class to represent a character.
    char_id: id as in the database
    story_id: id of the story
    stats: dictionary that includes the keys:
        name: character's name
        gender: 0=female, 1=male, 2=unknown
        birthday: text dd/mm/YY
        age: character's age
        height: integer cm
        weight: integer kg
        appearance: string that describes character's appearance
        personality: string that describes character's personality
        history: string that describes character's history
        picture: name of the picture, pictures are stored in characters/lib/avatars
        trivia: additional information on the character

    Returns:
        Character: returns a character object.
"""

from services.story_service import story_service


class Character:
    def __init__(self, char_id: int, story_id: int, stats: dict) -> None:
        self.char_id = char_id
        self.story_id = story_id
        self.stats = stats

    def name(self) -> str:
        """Character's name.

        Returns:
            str: Name of the character.
        """

        return self.stats["name"]

    def image(self) -> str:
        """Path to character's avatar.

        Returns path to the default picture, if the character doesn't have an avatar.

        Returns:
            str: Path to character's avatar.
        """

        pic = self.stats["picture"] or "default"
        return f"../library/avatars/{pic}.png"

    def gender(self) -> str:
        """String representantion of character's gender.

        Returns:
            str: Character's gender.
        """

        return {
            "0": "Female",
            "1": "Male",
            "2": "Unknown"
        }[str(self.stats["gender"])]

    def age(self) -> str:
        """String representation of character's age.

        Returns ??? if age isn't set.

        Returns:
            str: Character's age.
        """

        age = self.stats["age"]
        if age == 0:
            return "0"
        if age:
            return str(age)
        return "???"

    def birthday(self) -> str:
        """String representation of character's birthday.

        Returns ???? if birthday is completely unknown.
        Returns only day and month if year is unknown.

        Returns:
            str: Character's birthday.
        """

        birthday = self.stats["birthday"]
        if not birthday:
            return "Unknown"
        if birthday[-4:] == "????":
            return birthday[:-5]
        return birthday

    def height(self) -> str:
        """String representation of character's height.

        Not adding support for freedom units ever :D

        Returns:
            str: Character's height in centimeters.
        """
        h = self.stats["height"]
        if h:
            return f"{h} cm"
        return "??? cm"

    def weight(self) -> str:
        """String representation of character's weight.

        Returns:
            str: Character's weight in kilograms.
        """

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
