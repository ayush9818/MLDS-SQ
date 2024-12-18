"""Common string utilities."""

pets = ["dogs", "cats", "birds", "lizards", "hamsters", "fish", "snakes", "horses",
        "goats", "cows", "sheep", "pigs", "chickens"]


def join_strings(strings: list[str], sep: str = " ") -> str:
    """Join a list of strings.

    :param strings: A list of strings to join together
    :param sep: A character separating each member of "strings", defaults to " "
    :return: A single string containing all the members of "strings"
    """
    return sep.join(strings)
