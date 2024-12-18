from collections import namedtuple, defaultdict, deque
from typing import List
import os
import io

d = {'a': 37, 'b': 42,

     'c': 927}

x = 123456789.123456789E123456789

very_long_variable_name = namedtuple("very_long_variable_name", ["foo", 'bar'])
if very_long_variable_name is not None and \
        very_long_variable_name.foo > 0 or \
        very_long_variable_name.bar:
    z = 'hello ' + 'world'
else:
    world = 'world'
    a = 'hello {}'.format(world)
    f = rf'hello {world}'
this = True
that = bool(not this)
if (this
        and that):
    # FIXME: https://github.com/psf/black/issues/26 for reference to this problem
    y = 'hello ''world'


class Foo  (object):
    def f(self):
        return 37 * -2

    def g(self, x, y=42):
        return y


def foo(a: List[int]):
    u = int(this)
    y = 27
    return a[42 - u: y**3]


def very_important_function(template: str, *variables, file: os.PathLike, debug: bool = False,):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, "w") as f:
        ...
# fmt: off
custom_formatting = [
    0,  1,  2,
    3,  4,  5,
    6,  7,  8,
]
# fmt: on
regular_formatting = [
    0, 1, 2,
    3, 4, 5,
    6, 7, 8,
]
