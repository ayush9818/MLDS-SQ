# Testing Activity

Included in the [activity folder](./activity/) is a simple python module with several basic functions ready for unit testing.

## Activity

You will need to create unit tests for the included module and ensure that the functions are working as expected (all tests pass).

Use `pytest` to write and run your tests.

Remember, test modules should be named `test_MODULE_NAME.py` where `MODULE_NAME` is the name of the source code file being tested. e.g. `test_example.py` in this case.

Additionally, unit test functions should be named `test_FUNCTION_NAME_x()` where `FUNCTION_NAME` is the source code function being tested and `x` is some identifier used to distinguish multiple tests for the same function.

## Using the Dockerfile

The included Dockerfile can be used to build and run an image with the example python code.

To build the image:

```shell
docker build -t testing-lab .
```

To run all tests with `pytest`:

```shell
docker run testing-lab
```

## Run locally

```shell
cd activity
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest
```

## Resources

Refer to [README](./README.md) for guidance in writing tests

You can also refer to the [Pytest documentation](https://docs.pytest.org/en/stable/getting-started.html#create-your-first-test)

And the document on how to structure your python project for easy testing: [Pytest Good Practices](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html)