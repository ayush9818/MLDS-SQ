# Introduction to Pipx

Pipx is a tool for installing and running Python applications in isolated environments. It was designed to make it easier to install and manage Python applications that provide command-line interfaces (CLIs).

Pipx uses virtual environments to isolate applications from each other and from the system Python environment. This ensures that applications have access to the correct versions of dependencies, and that they don't interfere with other applications or the system Python environment.

With Pipx, you can install Python applications with a single command, and run them from anywhere on your system.

Docs: <https://pypa.github.io/pipx/>

Install Guide: <https://pypa.github.io/pipx/installation/>

## Basic functionality of Pipx

Pipx has two main functions: installing Python applications and running them.

### Install

To install an application with Pipx, you use the `pipx install` command followed by the name of the package you want to install. For example, to install the `black` code formatter, you would enter the following command:

```shell
pipx install black
```

This will create a virtual environment for the `black` application and install it in that environment. Once it is installed, it will be available in your system path and can be run natively as:

```shell
black
```

Note, if you install black in a virtual environment and then activate it, running `black` will run from the virtual environment (not from the `pipx` installed version) since the virtual environment will be first on your system `$PATH`. You can verify this by the following:

```shell
which black
python -m venv .venv
source .venv/bin/activate
pip install black
which black

# cleanup
deactivate
rm -rf .venv
```

### Run

To run an application installed with Pipx, you use the `pipx run` command followed by the name of the application. For example, to run the `black` code formatter, you would enter the following command:

```shell
pipx run black
```

This will download and run the `black` application within a temporary virtual environment, using the correct versions of dependencies.

Note, executing programs with the `run` command will cache that program for up to 14 days before cleaning it out. This is great for tools you want to try out or may use very rarely; things you rely on often should probably be `install`ed

## Important commands in Pipx

Here are some of the most important commands in Pipx:

- `pipx install`: Installs a Python application in a virtual environment.
- `pipx uninstall`: Uninstalls a Python application and its virtual environment.
- `pipx upgrade`: Upgrades a Python application to the latest version.
- `pipx list`: Lists all Python applications installed with Pipx.
- `pipx run`: Runs a Python application within its virtual environment.

## Conclusion

Pipx makes it super easy to install common python applications that you likely will want access to regardless of virtual environment. Things like `black`, `pylint`, and `pipenv` are good examples of this. However, packages that may rely on project dependencies or specific versions like `pytest`, `pandas`, and `mypy` may not be good candidates for pipx.
