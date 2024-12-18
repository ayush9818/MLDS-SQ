# Dataclasses

Want to take your type annotations to the next level? Tired of writing clunky boilerplate classes with
lengthy `__init__(self, ...)` definitions? Want to impress your friends with use of Python `@decorators`?
[Dataclasses](https://docs.python.org/3/library/dataclasses.html) are a great way to accomplish all of this and more!

A Dataclass is a simple decorator that makes it a breeze to declare complex types (or `structs` if you come from
computer science) and keep your code tight and tidy.

If you're not familiar with `@decorators` in Python, don't worry too much about it now as it's trivial to use
the `@dataclass` decorator.

The following example is taken from the excellent tutorial
on [Data Classes - RealPython](https://realpython.com/python-data-classes/).

```python
from dataclasses import dataclass


@dataclass
class DataClassCard:
    rank: str
    suit: str
```

```text
>>> queen_of_hearts = DataClassCard('Q', 'Hearts')
>>> queen_of_hearts.rank
'Q'

>>> queen_of_hearts
DataClassCard(rank='Q', suit='Hearts')

>>> queen_of_hearts == DataClassCard('Q', 'Hearts')
True
```

To define such a handy class yourself would require much more code:

```python
class RegularCard
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(rank={self.rank!r}, suit={self.suit!r})')

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.rank, self.suit) == (other.rank, other.suit)
```
