# Python Packages

## Project Structure

Structure of your python project is important! Not just because it determines how your code will be run and what commands you will use, but also just for the general organization of your thoughts and how users will understand your project. Most python projects follow a somewhat standard format, but this will depend greatly on the complexity of your project. However, it may be a good idea to get in the habit of creating a standard structure, even if you have a super simple project.

There is lots of content online with guidance on this topic:

- Python.org: <https://packaging.python.org/en/latest/tutorials/packaging-projects/>
- RealPython: <https://realpython.com/python-application-layouts/>
- Hitchhiker's Guide to Python: <https://docs.python-guide.org/writing/structure/>
- Some Dude who proposed a simple project structure 13 years ago: <https://github.com/navdeep-G/samplemod>

Obviously, you can use a cookiecutter template like we reviewed in the [cookiecutter example](../cookiecutter/README.md). However, `poetry` can also help you create a basic project structure with `poetry new ...`

## Building your python package

Python wheels are a built-package format for Python that simplify the installation of software. A wheel is essentially a ZIP archive containing the necessary files for a Python package. They are intended to make distribution of Python software easier and faster by providing pre-built, pre-compiled versions of packages that can be installed with a single command. Wheels can be installed using pip, the default package installer for Python. By using wheels, developers can easily distribute their Python packages with all the necessary dependencies, making it easier for users to install and use their software.

## Example

Create a new python project called example

```shell
poetry new example
```

Add some code to a file example/helpers.py

```python title=example/helpers.py
import typing

Number = typing.Union[int, float]


def sum(numbers: list[Number]) -> Number:
    total: Number = 0
    for n in numbers:
        total += n

    return total

```

Add a few development dependencies

```shell
poetry add -G dev ipython rich black
```

Install the project and all its dependencies

```shell
poetry install
```

Activate the virtual environment, and test it out

```shell
poetry shell
```

Add 

```python title=example/__init__.py
import example.helpers

__all__ = [example.helpers]
```

