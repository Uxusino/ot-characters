from repositories.db_management import db
from entities.character import Character

# This class is a stepping stone between database and Character as an object.
# This class will also be responsible for checking if user's input
# is valid or not.


class CharacterService():
    def __init__(self) -> None:
        pass

    def _convert_gender(self, gender: str) -> int:
        return {
            "Female": 0,
            "Male": 1,
            "Unknown": 2,
        }[gender]

    def _parse_gender(self, gender: str) -> int:
        if not gender or gender not in ["Female", "Male", "Unknown"]:
            return 2
        return self._convert_gender(gender=gender)

    # dd/mm/yyyy
    # All values must be numeric, else it will be reverted to unknown value
    def _parse_birthday(self, birthday: tuple[str]) -> str:
        day = birthday[0]
        month = birthday[1]
        year = birthday[2]

        if not day or not day.isnumeric():
            day = "??"
        if not month or not month.isnumeric():
            month = "??"
        if not year or not year.isnumeric():
            year = "????"

        birthday = f"{day}/{month}/{year}"
        if birthday == "??/??/????":
            return "Unknown"
        return birthday

    def _parse_number_value(self, value: str) -> int:
        if not value or not value.isnumeric():
            return None
        return int(value)

    def _parse_name(self, name: str) -> str:
        if not name:
            return "Unknown"
        return name

    # Adds character to database and returns a Character object
    def create_character(self, stats: tuple, story_id: int) -> Character:
        # You need to fill at least one field to create character.
        if not stats:
            return None
        for stat in stats:
            if not (not stat or stat == (None, None, None)):
                break
        else:
            return None

        name = self._parse_name(name=stats[0])
        gender = self._parse_gender(stats[1])
        birthday = self._parse_birthday(stats[2])
        age = self._parse_number_value(stats[3])
        height = self._parse_number_value(stats[4])
        weight = self._parse_number_value(stats[5])
        picture = stats[9]

        char_id = db.create_character((
            story_id,
            name,
            gender,
            birthday,
            age,
            height,
            weight,
            stats[6],   # Appearance
            stats[7],   # Personality
            stats[8],   # History
            picture,
            stats[10]   # Trivia
        ))

        if not char_id:
            return None

        new_char = Character(
            char_id=char_id,
            story_id=story_id,
            stats={
                "name": name,
                "gender": gender,
                "birthday": birthday,
                "age": age,
                "height": height,
                "weight": weight,
                "appearance": stats[6],
                "personality": stats[7],
                "history": stats[8],
                "picture": picture,
                "trivia": stats[10]
            }
        )

        return new_char

    def get_characters_by_story_id(self, story_id: int) -> list[Character]:
        db_characters = db.get_characters_by_story_id(story_id=story_id)
        if not db_characters:
            return None
        characters = []
        for c in db_characters:
            character = Character(
                char_id=c["char_id"],
                story_id=c["story_id"],
                stats=c["stats"]
            )
            characters.append(character)
        return characters


char_service = CharacterService()
