"""A stepping stone between database and Character as an object.

    Returns:
        CharacterService: App logic for everything to do with characters.
"""

from PIL import Image
from repositories.db_characters import char_db
from repositories.file_management import rep
from entities.character import Character
from services.formatter import formatter


class CharacterService():
    def __init__(self) -> None:
        pass

    def create_character(self, inf: tuple, story_id: int) -> Character:
        """Adds character to the database and returns a Character object.

        Args:
            inf (tuple): Tuple that contains all the character's info.
            story_id (int): Story id.

        Returns:
            Character: Character object.
        """

        if not inf:
            return None

        name = inf[0] or "Unknown"
        gender = formatter.convert_gender(inf[1])
        bday = formatter.parse_birthday(inf[2])
        age = formatter.parse_number_value(inf[3])
        ht = formatter.parse_number_value(inf[4])
        wt = formatter.parse_number_value(inf[5])
        appr = inf[6] if inf[6] != "" else None
        prsn = inf[7] if inf[7] != "" else None
        hist = inf[8] if inf[8] != "" else None
        triv = inf[10] if inf[10] != "" else None

        char_id = char_db.create_character((story_id, name, gender, bday, age,
                                            ht, wt, appr, prsn, hist, inf[9], triv))

        if not char_id:
            return None

        new_char = Character(
            char_id=char_id,
            story_id=story_id,
            stats={
                "name": name,
                "gender": gender,
                "birthday": bday,
                "age": age,
                "height": ht,
                "weight": wt,
                "appearance": appr,
                "personality": prsn,
                "history": hist,
                "picture": inf[9],
                "trivia": triv
            }
        )

        return new_char

    def update_character(self, stats: tuple[str | Character]) -> None:
        """Updates character information in the database.

        Args:
            stats (tuple): New information to be updated.
        """

        gender = formatter.convert_gender(stats[0])
        birthday = stats[1]
        age = formatter.parse_number_value(stats[2])
        height = formatter.parse_number_value(stats[3])
        weight = formatter.parse_number_value(stats[4])
        char_id = stats[5].char_id
        char_db.update_character(
            (gender, birthday, age, height, weight, char_id))

    def update_image(self, character: Character, img: Image) -> None:
        """Updates character's avatar.

        Args:
            character (Character): Character
            img (Image): New image
        """

        old_image = character.stats["picture"]
        new_image = rep.save_image(img)
        char_db.update_image(new_image, character.char_id)
        rep.delete_avatar(old_image)

    def get_characters_by_story_id(self, story_id: int) -> list[Character]:
        """Searches all characters of a certain story in the database.

        Args:
            story_id (int): Story id.

        Returns:
            list[Character]: Contains Character-objects.
        """

        db_characters = char_db.get_characters_by_story_id(story_id=story_id)
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

    def get_image_path(self, character: Character) -> str:
        """Creates file path for character's avatar.

        Args:
            character (Character): Character whose avatar we're getting.

        Returns:
            str: Complete path to the image.
        """

        img_path = character.image()
        return rep.get_file_path(img_path)

    def get_relations(self) -> list[str]:
        """All relation names as a list.

        Returns:
            list[str]: List with relation names.
        """

        return char_db.get_relations()

    def get_character_relations(self, character: Character) -> list[tuple]:
        """Searches all relationships of a character.

        Args:
            character (Character): Character whose relationships we're searching.

        Returns:
            list[tuple]: List with all relationships of this character.
        """

        relations = char_db.get_character_relations(character.char_id)
        return relations

    def set_relations(self, char1: Character, char2: Character, relation: str, former: int) -> None:
        """Set a relationship between two characters.

        Char2 is ___ to char1.

        Args:
            char1 (Character): First character.
            char2 (Character): Second character.
            relation (str): Relation name
            former (int): Is relation former or not? 1 or 0
        """

        char1_id = char1.char_id
        char2_id = char2.char_id
        rel_id = char_db.get_relation_id_from_name(relation)
        char_db.set_relation(char1_id=char1_id, char2_id=char2_id,
                             relation_id=rel_id, former=former)

    def delete_character(self, character: Character) -> None:
        """Deletes character from the database.

        Args:
            character (Character): Character object
        """

        char_db.delete_character(character.char_id)
        char_db.delete_character_relations(character.char_id)
        if character.stats["picture"]:
            rep.delete_avatar(character.stats["picture"])

    def clear_characters(self) -> None:
        """Deletes all characters and their avatars.
        """

        char_db.clear_characters()
        rep.delete_all_avatars()


char_service = CharacterService()
