# Typehints and Linters

This lab will cover the usage of Python typehints and linters to improve code quality and maintainability.

---

## [Typehints](./typehints/README.md)

Python is a _dynamically typed_, _interpreted_ language. This makes it very good at certain tasks (scripting, data
exploration, etc.) and also makes it a very approachable language. However, these same advantages can make building
large, complicated applications or pipelines difficult and error-prone.

To help remedy this, Python introduced **_typehints_** along with version `3.5`.

Typehints do **not** enforce static types at runtime, but they **do** add information to your python code that can be
interpreted by the developer and many third-party tools.

[More information and detailed examples included in the typehints README](./typehints/README.md)

---

## [Linters](./linting/README.md)

Linters are commonly used across all types of software engineering projects and all coding languages to help developers
write cleaner, more stylistic code that others can easily read and maintain.

Linters are essentially parsing engines coupled with rule sets that allow for static analysis of your code and alert you
to any violations of those rules. The rules mentioned here usually include a default set of style rules (suggestions)
made by the language or linter maintainers, as well as any custom rules you want to provide. Almost all linters are
highly customizable so that you can supply a config file for a project and ensure that all the contributors are
implementing the same consistent style across the project's codebase.

[More information and detailed examples included in the linting README](./linting/README.md)
