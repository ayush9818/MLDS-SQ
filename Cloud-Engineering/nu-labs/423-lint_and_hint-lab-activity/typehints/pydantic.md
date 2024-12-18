# Pydantic

## Introduction

In software development, it's important to ensure that the data being passed around in your program is valid and meets certain criteria. [Pydantic](https://docs.pydantic.dev/) is a Python library that makes this task easier by providing a simple and intuitive way to define data models and validate data based on Python type annotations. It is especially useful for data scientists who need to work with structured data. Another strong use-case is for validating dynamic data such as requests from users of a web application as you have already seen in our FastAPI examples.

Pydantic allows you to define a model by creating a class that inherits from the `pydantic.BaseModel` class. In this class, you define the attributes of your data, their types, and optionally specify validation rules. Pydantic then automatically validates the data that you pass to the model based on the type annotations and any validation rules you have specified. It can also be used for managing settings by defining a model with default values, and Pydantic will automatically read the values from environment variables or a configuration file.

### Comparison to Python Dataclasses

Python dataclasses are a built-in feature that provides a way to define classes with automatically generated methods such as `__init__`, `__repr__`, and `__eq__`. While dataclasses are useful for defining classes with simple attributes, they don't provide built-in validation or settings management.

In contrast, Pydantic is specifically designed for data validation and settings management. It allows you to define models with validation rules, making it easy to ensure that the data being passed around in your program is valid. It also provides a simple way to manage settings with default values, making it easy to read values from environment variables or configuration files.

## In Practice

1. Installing Pydantic: Open your terminal or command prompt and install Pydantic using the following command:

    ```shell
    pip install pydantic
    ```

2. Defining a Pydantic Model: In Pydantic, you define a model by creating a class that inherits from the `pydantic.BaseModel` class. In this class, you define the attributes of your data, their types, and optionally specify validation rules.

    ```python
    from pydantic import BaseModel

    class User(BaseModel):
        id: int
        name: str
        email: str
    ```

    Here, we define a simple `User` model with `id`, `name`, and `email` attributes.

3. Creating an Instance of the Model: To create an instance of our `User` model, we can simply pass the values to its constructor:

    ```python
    user = User(id=1, name='John Doe', email='john.doe@example.com')
    print(user)
    ```

    This will output:

    ```log
    User id=1 name='John Doe' email='john.doe@example.com'
    ```

4. Validation: Pydantic automatically validates the data that you pass to the model based on the type annotations and any validation rules you have specified. For example, if we try to create a `User` instance with an invalid type for `id`, we will get a validation error:

    ```python
    user = User(id='invalid', name='John Doe', email='john.doe@example.com')
    ```

    This will raise a `pydantic.error_wrappers.ValidationError` with the error message:

    ```log
    1 validation error for User
    id
    value is not a valid integer (type=type_error.integer)
    ```

5. Settings Management: Pydantic can also be used for managing settings. You can define a model for your settings with default values, and Pydantic will automatically read the values from environment variables or a configuration file:

    ```python
    from pydantic import BaseSettings

    class Settings(BaseSettings):
        app_name: str = 'My App'
        max_items: int = 10

    settings = Settings()
    print(settings.app_name)
    print(settings.max_items)
    ```

    Here, we define a `Settings` model with `app_name` and `max_items` attributes, with default values of `'My App'` and `10`, respectively. Pydantic will read the values from environment variables with the same name as the attributes, or from a `.env` file in the current directory.

    <!-- TODO: Add env var examples -->

## Conclusion

Pydantic is a powerful library for data validation and settings management in Python. It provides a simple and intuitive way to define data models and validate data based on Python type annotations. It is also easy to use for managing settings in your Python applications.
