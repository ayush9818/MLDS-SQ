# Introduction to Poetry

Poetry is a tool for managing dependencies in Python projects. It provides a modern approach to dependency management, with features like dependency resolution, virtual environments, and version control integration.

With Poetry, you can easily manage your project's dependencies, including installing and updating packages, creating virtual environments, and publishing packages to PyPI.

Docs: <https://python-poetry.org/docs/basic-usage/>

Install Guide: <https://python-poetry.org/docs/#installation>

## Important commands in Poetry

Here are some of the most important commands in Poetry:

- `poetry init`: Initializes a new Python project with a `pyproject.toml` file.
- `poetry install`: Installs the project's dependencies from the `pyproject.toml` file.
- `poetry add`: Adds a new dependency to the project.
- `poetry remove`: Removes a dependency from the project.
- `poetry update`: Updates the project's dependencies to their latest compatible versions.
- `poetry run`: Runs a command within the project's virtual environment.
- `poetry shell`: Starts a new shell session within the project's virtual environment.
- `poetry publish`: Publishes the project to PyPI.

## Groups in Poetry

One of the features that sets Poetry apart from other Python dependency management tools is its support for "groups". Groups allow you to define different sets of dependencies for different use cases or environments, such as development, testing, or production.

To use groups in Poetry, you can define a `[tool.poetry.group]` section in your `pyproject.toml` file. Here's an example:

```toml
[tool.poetry.group.dependencies]
requests = "*"
django = { version = "^3.2", extras = ["bcrypt"] }

[tool.poetry.group.dev-dependencies]
pytest = "^6.2"
flake8 = "^4.0"

[tool.poetry.group.extras]
fastapi = ["fastapi", "uvicorn"]
```

In this example, we have three groups defined:

- `dependencies`: Contains the packages that are required for the project to run. Here, we're using the `requests` package and specifying a specific version of `django` with an extra dependency of `bcrypt`.
- `dev-dependencies`: Contains packages that are only required during development and testing. Here, we're using the `pytest` and `flake8` packages.
- `extras`: Contains packages that are optional and only required for specific features or use cases. Here, we're defining an extra called `fastapi` that includes the `fastapi` and `uvicorn` packages.

You can then install the packages for a specific group using the `poetry install` command with the `--group` option. For example, to install only the packages required for development, you would run:

```shell
poetry install --no-root --extras "fastapi" --group dev-dependencies
```

This will install only the packages defined in the `dev-dependencies` group, along with any extras defined in the `fastapi` group.

Using groups in Poetry can help you manage your project dependencies more effectively, and make it easier to switch between different environments or use cases.

## Example

```shell
poetry new
```

This command will help you kickstart your new Python project by creating a directory structure suitable for most projects.

---

```shell
poetry init
```

This command will help you create a `pyproject.toml` file interactively by prompting you to provide basic information about your package.

---

```shell
poetry install
```

The `install` command reads the `pyproject.toml` file from the current project, resolves the dependencies, and installs them.

---

```shell
poetry add
```

The `add` command adds required packages to your `pyproject.toml` and installs them.

If you do not specify a version constraint, poetry will choose a suitable one based on the available package versions.

---

```shell
poetry run
```

The `run` command executes the given command inside the project’s virtualenv.

It can also execute one of the scripts defined in `pyproject.toml`.

---

```shell
poetry shell
```

The `shell` command spawns a shell, according to the `$SHELL` environment variable, within the virtual environment. If one doesn’t exist yet, it will be created.

---

```shell
poetry export -f requirements.txt --output requirements.txt
```

This command exports the lock file to other formats.

---

```shell
poetry show
```

To list all the available packages, you can use the show command.

If you want to see the details of a certain package, you can pass the package name.

## Note on `pyproject.toml`

The `pyproject.toml` file is a configuration file for Python projects, and is used by various tools in the Python ecosystem such as Poetry, Flake8, Black, and others. This file can include various settings and configurations for your project, including dependencies, scripts, and other settings.

More importantly, `pyproject.toml` is now the standard way to define metadata for your python project (replaces `setup.py`). With a proper `pyproject.toml` file, you can install your project locally, share your project with others, and publish your package to `pypi` or another package index.

Here are some of the main sections you might find in a `pyproject.toml` file:

### `[tool.poetry]`

This section is used by the Poetry dependency management tool to manage your project's dependencies. Here, you can define your project's name, version, description, author information, and dependencies. You can also define development dependencies, specify package extras, and configure various other settings.

### `[tool.black]`

This section is used to configure the Black code formatter. Here, you can specify the line length, how to handle string formatting, and other options.

### `[tool.mypy]`

This section is used to configure the Mypy type checker. Here, you can specify which files to check, which type checking options to use, and other options.

### `[build-system]`

This section is used to define how your project should be built and packaged. Here, you can specify the build tool to use (such as setuptools or flit), the minimum version of Python required to run your project, and other options.

### `[project]`

This section includes basic information about your project. An example (and more info) can be found in the Python [PEP-621](https://peps.python.org/pep-0621/#example)

```ini
[project]
name = "The name of your project."
version = "The version number of your project."
description = "A short description of your project."
license = "The license under which your project is released."
authors = "A list of the authors of the project, in the format `name <email>`."
maintainers = "A list of the maintainers of the project, in the format `name <email>`."
readme = "The file name of the project's readme file."
dependencies = "A list of the project's dependencies."
dependencies = "A list of the project's development dependencies."
extras = "A dictionary of optional dependencies, organized by "extra" names."
scripts = "A dictionary of command-line scripts that can be run using the `poetry run` command."
plugins = "A dictionary of plugin dependencies."
source = "The URL or path to the project's source code."
homepage = "The URL to the project's homepage."
repository = "The URL to the project's code repository."
keywords = "A list of keywords associated with the project."
```

These are just some of the fields that may be found in a `pyproject.toml` file. The fields you use will depend on the needs of your project and the tools you're using to manage it.

## Conclusion

Poetry is a powerful tool for managing dependencies in Python projects. With its modern approach to dependency management and powerful features, you can easily manage your project's dependencies, create virtual environments, and publish packages to PyPI. With the basic functionality and important commands outlined in this guide, you can start using Poetry to manage your Python projects.
