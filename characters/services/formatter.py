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

        if not text:
            return ""

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

    def parse_number_value(self, value: str) -> int:
        """If user has given non-numeric value, resets it to None.

        Args:
            value (str): String value that must represent a number.

        Returns:
            int: Integer representation of given numeric string.
        """

        if not value or value == "":
            return None

        _value = value.split()[0]
        num_value = ""
        for sym in _value:
            if sym.isnumeric():
                num_value = num_value + sym
        if num_value == "":
            return None
        return int(num_value)

    def convert_gender(self, gender: str) -> int:
        """Converts gender from string to integer representative.

        0 = Female
        1 = Male
        2 = Unknown/other

        Args:
            gender (str): Gender string

        Returns:
            int: Integer representative of character's gender.
        """

        if not gender or gender.lower() not in ["female", "male", "unknown", "0", "1", "2", "f", "m"]:
            return 2
        return {
            "female": 0,
            "0": 0,
            "f": 0,
            "male": 1,
            "m": 1,
            "1": 1,
            "unknown": 2,
            "2": 2
        }[gender.lower()]

    def parse_birthday(self, birthday: tuple[str]) -> str:
        """Converts day, month and year to string representation of birthday.

        All values must be numeric, else it will be reverted to an unknown value.

        Args:
            birthday (tuple[str]): Tuple with values of day, month and year.

        Returns:
            str: Birthday in the form of dd/mm/yyyy
        """
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
            return None
        return birthday


formatter = Formatter()
