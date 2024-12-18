# Pipenv Tutorial

Pipenv is a popular tool for managing Python packages and virtual environments. It combines the functionality of pip (Python's package installer) and virtualenv (Python's virtual environment tool) in a single tool. This guide will cover the basics of how to use Pipenv to manage packages and virtual environments in your Python projects.

Docs: <https://github.com/pypa/pipenv#usage>, <https://pipenv.pypa.io/en/latest/>, <https://realpython.com/pipenv-guide/>

Install Guide: <https://pipenv.pypa.io/en/latest/installation/>

## Installing Pipenv

To use Pipenv, you first need to install it. You can install Pipenv using pip, the Python package installer. Open a terminal or command prompt and enter the following command:

```shell
pipx install pipenv
# or
pip install --user pipenv
```

## Creating a new project with Pipenv

To create a new Python project using Pipenv, navigate to the directory where you want to create your project and enter the following command:

```shell
pipenv --python 3.9
```

This will create a new virtual environment for your project using Python version 3.9. If you don't specify a Python version, Pipenv will use the system's default version.

Next, you can install packages for your project using the `pipenv install` command. For example, to install the `numpy` package, enter the following command:

```shell
pipenv install numpy
```

This will install the `numpy` package and add it to your project's Pipfile, which is used to track your project's dependencies.

## Running commands in a virtual environment

Pipenv allows you to run commands within the context of your virtual environment using the `pipenv run` command. This is useful for running scripts or commands that require certain packages to be installed.

To run a command with Pipenv, simply prefix the command with `pipenv run`. For example, to run a Python script within the context of your virtual environment, enter the following command:

```shell
pipenv run python script.py
```

This will run the `script.py` file within the context of your virtual environment, using the packages installed in your Pipfile.

You can also use `pipenv run` to run other commands, such as `pip`, `pytest`, or `flake8`. For example, to run the `pytest` command within the context of your virtual environment, enter the following command:

```shell
pipenv run pytest
```

This will run the `pytest` command within the context of your virtual environment, using the version of `pytest` installed in your Pipfile.

Note, if you are skeptical of the environment's "activeness", you can verify by running:

```shell
pipenv run which python
```

## Conclusion

The `pipenv run` command is a useful tool for running commands within the context of your virtual environment. By using `pipenv run`, you can ensure that your commands are using the correct versions of packages installed in your Pipfile.

## Activating a virtual environment

When you create a new project with Pipenv, it automatically creates a virtual environment for your project. To activate the virtual environment, enter the following command:

```shell
pipenv shell
```

This will activate the virtual environment and switch your terminal or command prompt to the virtual environment's shell. You can now run Python and install packages as usual.

## Environment Variables

Note, one of the cool features in `pipenv` is that the `.env` file in your project will be automatically loaded into your session whenever you execute `pipenv run` commands or `pipenv shell`.

## Managing packages with Pipenv

To install a package for your project, use the `pipenv install` command followed by the package name. For example, to install the `requests` package, enter the following command:

```shell
pipenv install requests
```

This will install the `requests` package and add it to your project's Pipfile. To remove a package, use the `pipenv uninstall` command followed by the package name. For example, to remove the `requests` package, enter the following command:

```shell
pipenv uninstall requests
```

You can also use the `pipenv lock` command to generate a `Pipfile.lock` file, which is used to lock the versions of your project's dependencies. This ensures that everyone working on the project is using the same versions of the packages.

## Conclusion

Pipenv is a powerful tool for managing Python packages and virtual environments. It simplifies the process of creating new projects, managing packages, and activating virtual environments. It can add a lot of clarity to your project and make make for convenient development; however, it is a less popular environment manager and thus you may have to explain it to users.
