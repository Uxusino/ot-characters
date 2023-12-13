class Formatter:
    """Formatter serves for parsing and formatting strings.
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


formatter = Formatter()
