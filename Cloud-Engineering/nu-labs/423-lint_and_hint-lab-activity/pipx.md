# pipx

Install and Run Python Applications in Isolated Environments

The following content is entirely extracurricular, but I think can be helpful in managing your Python virtual
environments, especially as we introduce Python CLI (Command Line Interface) applications which are used globally across
many projects.

## Context

Many tools are built with Python and packaged/distributed on the pypi package repository (installed via `pip`). This is
the same place you would go to install libraries and other packages that you would use _in_ your Python code.

Whereas a _library_ is only useful when called by Python code and run inside a Python environment alongside other
project dependencies, an _application_, or _tool_ can be run from the command line regardless of environment.

## What is `pipx`

This section is taken straight from the [pipx docs](https://pypa.github.io/pipx/#overview-what-is-pipx)

### Overview

pipx is a tool to help you install and run end-user applications written in Python. It's roughly similar to macOS's
brew, JavaScript's npx, and Linux's apt.

It's closely related to pip. In fact, it uses pip, but is focused on installing and managing Python packages that can be
run from the command line directly as applications.

## How is it Different from pip?

pip is a general-purpose package installer for both libraries and apps with no environment isolation. pipx is made
specifically for application installation, as it adds isolation yet still makes the apps available in your shell: pipx
creates an isolated environment for each application and its associated packages.

pipx does not ship with pip, but installing it is often an important part of bootstrapping your system.

## Installing `pipx`

See the [Installation Guide](https://pypa.github.io/pipx/installation/) for more detailed installation instructions.

`pipx` can be installed with `pip` by running the following:

```shell
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

## Using `pipx`

See more on the [pipx features page](https://pypa.github.io/pipx/#features)

`pipx` can be easily used to install Python CLI applications that are available on the pypi repository. One such useful
tool would be `mypy`, a typechecker tool that makes use of Python's typehints to perform static analysis of your code.

Install an application

```shell
pipx install mypy
which mypy
# /Users/mfedell/.local/bin/mypy
```

List all installed applications

```shell
pipx list
# venvs are in /Users/mfedell/.local/pipx/venvs
# apps are exposed on your $PATH at /Users/mfedell/.local/bin
#   package mypy 0.942, Python 3.9.4
#    - dmypy
#    - mypy
#    - mypyc
#    - stubgen
#    - stubtest
```
