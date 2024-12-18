# Virtual Environments

A Python Virtual Environment is a directory on your system that contains a particular version of python as well as any additional packages that are used.

This helps with a number of issues:

- messy system installation / risk of breaking core system tools
- specific version requirements differing across projects
- sharing a project's python setup with other collaborators
- ensuring that you can install and use packages in a consistent manner

The python standard docs also include [a tutorial on Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html)

## Important High Level Concepts

### System Path

Your system `$PATH` determines which programs are available by specifying the "search path" in which your shell will go looking for an executable file that matches the command you've supplied. The shell will go look in each location specified in `$PATH` in order, stopping when it finds the first match.

To check the contents of your `$PATH` variable, you can run:

```shell
echo $PATH | tr ":" "\n"
```

### Python Path

Your Python PATH is similar in that it contains the locations python will go looking for modules that you try to import.

1. current working directory
2. list of directories in `$PYTHONPATH`
3. list of directories relative to the installation of python executable

Usually we only care about 1 and 3 as we don't often set 2. If we are importing modules that we are writing (or using relative imports, `1` will likely be where these are found). For packages installed by pip, these are usually found in `3` which is often the `site-packages` directory.

```shell
which python
python -c "import sys; print('\n'.join(sys.path))"
python -c "import site; print('\n'.join(site.getsitepackages()))"
```

### Environment Variables

Environment variables are flexible key-value pairs that you can set in a shell session to control various programs, store data, and configure your shell. They typically use UPPER_SNAKE_CASE for the names and the values are always strings. Env vars (short) are ephemeral within your shell session; once you close the session, any env vars that you set will be removed. In order to have one be preserved from one session to another, you must define it in your shell configuration file (`.profile`, `.bashrc`, `.zshrc`, etc. based on your shell).

These will have an important impact on your environment as you run commands!

It is pretty common to also keep secret things in environment variables such as API Keys, AWS Credentials, Database passwords, etc. These are usually all kept in a file that is ignored from git (commonly `.env`).

There is a pretty popular python tool for working with these `.env` files: [`python-dotenv`](https://github.com/theskumar/python-dotenv).

## Virtual Environment Managers

A number of solution exist for managing virtual environments and installing packages. You are likely already familiar with a few of them.

`pip` is a package manager, it handles the installation of packages and their dependencies
`venv` is an environment manager, it helps you create isolated virtual environments into which packages can be installed
`conda` is both an environment manager and a package manager and includes commands for both features

Additionally, you may come across:

- `virtualenv`: a separate tool installed by pip for creating virtual environments (replaced by python standard `venv`) ([see more](https://docs.python.org/3/library/venv.html))
- `pipenv`: a pip-based dual-function environment/package manager (similar to conda) ([see more](https://pypi.org/project/pipenv/) and [why pipenv](https://realpython.com/pipenv-guide/))
- `poetry`: a package manager with a focus on developing/building/publishing packages ([see more](https://python-poetry.org/docs/))

as well as:

- `pyenv`: a tool for managing python versions installed to your machine ([see more](https://github.com/pyenv/pyenv))
- `pipx`: a tool for installing applications (as opposed to libraries) from pip into isolated environments available globally ([see more](https://pypi.org/project/pipx/))

You can try out any of these tools (or others) and decide which works best for you, the important thing is that you decide on and make use of a virtual environment strategy. **THIS IS VERY IMPORTANT**!

## Dependency Files

There are several ways to track and control the packages installed to a particular environment. The most common (standard) way of doing so is with a `requirements.txt` file. This file can be created/managed manually, or automatically created by `pip` based on an active environment (`pip freeze`). Pip can install dependencies from this file via `pip install -r requirements.txt`.

Conda has it's own command and format for creating and using dependency files. This is often named `environment.yaml` (or `environment.yml`) and is created with `conda env export > environment.yaml`. A new environment can be created from file via `conda create -n env_name -f environment.yaml`.

Pipenv also has it's own file format that is actually quite different from the first two. Instead of sticking all packages (manually installed packages and automatically installed requirements) in the same file, it keeps a clean `Pipfile` (toml format) with requested packages (and the versions specified during install), and a separate `Pipfile.lock` with all the sub requirements and specific versions/builds that were used. This is managed via `pipenv install ...` (which both installs the package and immediately adds it to the `Pipfile`).

Poetry takes a similar approach, but uses the new python-adopted file format `pyproject.toml`.

## Listing project dependencies with `requirements.txt`

Every github repository and/or software based project using Python should have a `requirements.txt` file that includes all of the Python package dependencies of the project. This list should have no more and no less packages than are necessary to build an environment from scratch and execute the project code.

### Creating a `requirements.txt`

All Python packages necessary for a project should be added to the `requirements.txt` file using the following format:

```text
python-package-name==0.1.2
```

where `0.1.2` is the version of the Python package used to develop the project. You can use `conda list` or `pip list` to find the version numbers that you are using.

You will see in a lot of documentation that you can use

```bash
pip freeze > requirements.txt
```

to create the `requirements.txt` file. However, this freezes not only the exact versions of the packages you have explicitly installed but also the exact versions of the dependencies of those packages. However, those packages likely only have a dependency on the version being the current version or greater, e.g.:

```text
python-package-dependency-name>=1.2.3
```

but `pip freeze` will _freeze_ the dependency as:

```text
python-package-dependency-name==1.2.3
```

This more restrictive requirement could pose problems later on if you install additional packages in the environment that have a requirement such as:

```text
python-package-dependency-name>=1.2.4
```

You will run into a dependency issue if you add the new package because the `requirements.txt` will call for version 1.2.3 for `python-package-dependency-name` - even though it would be just fine with version 1.2.4.

One solution is to only add the python packages that you explicitly import in your code (manually create and manage `requirements.txt`). The other is to use a more robust environment management tool.

## Testing your `requirements.txt` with `venv`

Many of these tools are packed with features that simplify development and project management. However, they are quite heavy-weight and are generally not used in production. Therefore, to test that your requirements are adequate for your application, it is a good idea to use `venv`.

You can check that your `requirements.txt` works by doing the following:

```bash
# Create a virtual environment in the "test-env" folder
python -m venv test-env

# Activate the virtual environment, install your packages, and run your code
source test-env/bin/activate
pip install -r requirements.txt
pytest

# Deactivate the virtual environment and remove it
deactivate
rm -rf test-env
```

## Examples of Tools

- [Pyenv](./examples/pyenv/README.md): manage multiple python versions
- [Pipx](./examples/pipx/README.md): install isolated python executables
- [Venv + Pip](./examples/venv/README.md): basic python virtual environments
- [Conda](./examples/conda/README.md): complete python manager
- [Pipenv](./examples/pipenv/README.md): simple python environment/package manager
- [Poetry](./examples/poetry/README.md): feature rich python environment/package manager

## Resources

- [`conda` cheat sheet](http://know.continuum.io/rs/387-XNW-688/images/conda-cheatsheet.pdf)
- [`pip freeze` considered harmful](https://medium.com/@tomagee/pip-freeze-requirements-txt-considered-harmful-f0bce66cf895)
- [`conda` documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/overview.html)
- [Why you need Python environments and how to manage them with Conda](https://medium.freecodecamp.org/why-you-need-python-environments-and-how-to-manage-them-with-conda-85f155f4353c)
