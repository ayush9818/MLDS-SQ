import typing
import pandas as pd

number = typing.Union[int, float]


def add(first: int, second: int) -> int:
    return first + second


def add_numbers(first: number, second: number) -> number:
    print(type(first), type(second))
    return first + second


def sum_up(vals: list[int]):
    total: int = 0
    for val in vals:
        total += val
    return total


class Dog:
    def __init__(self, name: str, color: str, age: int):
        self.name = name
        self.color = color
        self.age = age


def print_dog(dog: Dog):
    print(dog.name + " is a " + dog.age + " year old " + dog.color + " dog")


def clean_dataframe(df: pd.DataFrame, fill_val: str) -> pd.DataFrame:
    return df.fillna(value=fill_val)


def count_children(df: pd.DataFrame, max_age: int = 18) -> int:
    return sum(df.age <= max_age)


if __name__ == "__main__":
    add(1, 2)
    add(1, 3.1)
    add(1, "two")

    val = "1"

    result = add_numbers(1, 2)
    val = add_numbers(1, 3.1)
    add_numbers(1, "two")

    d = Dog("fido", 2, "brown")

    d = Dog("fido", "brown", 2)
    print_dog(d)

    roster = pd.DataFrame({"name": ["alice", "bob", None], "age": [28, 12, 23]})
    print(roster)
    just_children = count_children(roster)
    just_children = clean_dataframe(just_children, "Unk")
