# Cookiecutter

`cookiecutter` is a tool for generating project directories based on a standardized template. A template can be injected with information specific to the author/project/etc. and then used in the generated files, directory names, etc.

This is an excellent tool to both save you time as well as add a great deal of standardization to your projects.

Docs: <https://cookiecutter.readthedocs.io/en/stable/README.html>

Installation: <https://cookiecutter.readthedocs.io/en/stable/installation.html>

## Main Functionality

There are two sides to cookiecutter:

- using existing templates to create new projects
- creating templates to be used by others

### Using Existing Templates

- How to find Python project templates
  - Search for templates on Github: <https://github.com/topics/cookiecutter-template>
- How to create a new project from a template
  - Run `cookiecutter <template-url>` in the command line
- How to fill in template placeholders
  - Answer prompts in the command line
  - Pass input as command-line arguments
- How to customize generated files
  - Edit the generated files directly
  - Use post-generate hooks to modify files

### Creating Your Own Templates

- Anatomy of a Cookiecutter template
  - `cookiecutter.json` file
  - Template files and folders
  - Placeholder syntax (`{{cookiecutter.placeholder_name}}`)
- Template metadata
  - `cookiecutter.json` fields for template metadata
  - `README.md` file with template documentation
- Advanced template customization options
  - Use Jinja2 templates to generate dynamic content
  - Use hooks to run scripts after generating a project

## Example

This is a template for python packages (although it includes quite a bit of complexity and extra tooling; also is a bit outdated):

[Cookiecutter Pypackage](https://cookiecutter-pypackage.readthedocs.io/en/latest/)

```shell
cookiecutter gh:audreyfeldroy/cookiecutter-pypackage
```

And here is yet another that is built more for data science projects:

[Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)

```shell
cookiecutter -c v1 gh:drivendata/cookiecutter-data-science
```
