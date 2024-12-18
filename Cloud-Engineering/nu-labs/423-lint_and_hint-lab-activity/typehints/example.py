from itertools import count
import pandas as pd


def add(first, second):
    return first + second


def add_numbers(first, second):
    print(type(first), type(second))
    return first + second


def sum_up(vals):
    total = 0
    for val in vals:
        total += val
    return total


class Dog:
    def __init__(self, name, color, age):
        self.name = name
        self.color = color
        self.age = age


def print_dog(dog):
    print(dog.name + " is a " + dog.age + " year old " + dog.color + " dog")


def clean_dataframe(df, fill_val):
    return df.fillna(value=fill_val)


def count_children(df, max_age=18):
    return sum(df.age <= max_age)


if __name__ == "__main__":
    add(1, 2)
    add(1, 3.1)
    add(1, "two")

    add_numbers(1, 2)
    add_numbers(1, 3.1)
    add_numbers(1, "two")

    d = Dog("fido", 2, "brown")

    d = Dog("fido", "brown", 2)
    print_dog(d)

    df = pd.DataFrame({"name": ["alice", "bob", None], "age": [28, 12, 23]})
    print(df)
    just_children = count_children(df)
    just_children = clean_dataframe(just_children, "Unk")
