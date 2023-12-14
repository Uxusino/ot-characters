class Formatter:
    """Formatter serves for parsing and formatting different types of data.
    """

    def __init__(self) -> None:
        self._ex_names = ["spouse", "wife", "husband",
                          "partner", "girlfriend", "boyfriend"]
        self._ex_convert = {
            "spouse": "ex-spouse",
            "wife": "ex-wife",
            "husband": "ex-husband",
            "partner": "ex",
            "girlfriend": "ex-girlfriend",
            "boyfriend": "ex-boyfriend"
        }

    def split_text(self, text: str, n: int) -> str:
        """Splits long text to different lines by n characters.

        Args:
            text (str): String to be splitted.

        Returns:
            str: Splitted string.
        """

        x = 0
        new_text = ""
        for y in text:
            if x > n and y == " ":
                new_text = new_text + "\n"
                x = 0
                continue
            new_text = new_text + y
            x += 1
        return new_text

    def relation_str(self, relationship: tuple) -> str:
        """Parses a relationship tuple into a string.

        Args:
            relationship (tuple): (Character's name, Former, Relationship's name)

        Returns:
            str: Parsed string that describes said relation.
        """

        former = relationship[1] == 1
        relationship_name = relationship[2]
        if relationship_name in self._ex_names and former:
            relationship_name = self._ex_convert[relationship_name]
            return f"{relationship[0]}: {relationship_name}."
        return f"{relationship[0]}: {relationship_name}. {'(former)' if former else ''}"

    def characters_to_dict(self, lst: list) -> list[dict]:
        """Converts list with raw characters data into a clean dictionary.

        Args:
            lst (list): Raw list with data from the database.

        Returns:
            list[dict]: Contains characters represented by a dictionary.
        """

        characters = []
        for c in lst:
            character = {
                "char_id": c[0],
                "story_id": c[1],
                "stats": {
                    "name": c[2],
                    "gender": c[3],
                    "birthday": c[4],
                    "age": c[5],
                    "height": c[6],
                    "weight": c[7],
                    "appearance": c[8],
                    "personality": c[9],
                    "history": c[10],
                    "picture": c[11],
                    "trivia": c[12]
                }
            }
            characters.append(character)
        return characters


formatter = Formatter()
