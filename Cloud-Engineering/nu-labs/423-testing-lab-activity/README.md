# Testing

The material included in this README is pulled from past years' lecture material for extended reference and information.

Interactive examples can be found in the `examples/` directory.

The lab activity can be found in the included [Activity.md](./Activity.md).

## What is a test ?

- Code or process that validates the functionality of your main application code
- Ran throughout development, before code is merged to master, and before the application is deployed to production.

## Why test ?

- Make sure your code/application is doing what you intend it to do
- Communicate intent of code to others
- Validate functionality across contexts (e.g. your local environment, deployment environment, another developer’s local environment)

# Types of testing

## Different types of testing

- Unit
- Integration
- System
- Acceptance

Note: For the purposes of this class we will focus on unit testing.

## Integration testing

Validates the interaction between components of a system
</br>
</br>

Examples of things that are integration tested:

* Components in a large application being built by different developers/teams
* How your applicaton queries and interacts with a database
* API calls to a web service

## System testing

Test the ability of an application or system to meet the given requirements. Examples include:

* An API endpoint being able to handle a certain amount of requests per minute
* The response time of a component that executes a database query
* An web service responding with the expected output schema

## Acceptence testing

Typically tests that the application or system behaves as the user expects and wants. Typically tests are executed by a product owner, the actual user(s), or using automation if the consumer is another applicaton/system.

# Unit testing

## Unit testing

A unit tests validates a small, specific part of your code like a function or method to ensure that the functionality of that specific unit of code is working as expected. Examples include:

- Testing that your function handles the expected input appropriately
- A class method executing a calculation correctly
- Validating that a function correctly parses input strings

## Unit testing guidelines

- Write and structure your code to make it easy to test
- Unit tests should be isolated and test specific functionality
- A single function can have one or more unit tests associated with it.
- Unit tests should be able to run indepedently and quickly.
- There are typically several unit tests in a set

## Unit testing guidelines

Avoid network (API) calls and database calls. Such calls introduce an element that is external to the unit of code that you are trying to test.  Testing with API and database calls is done during integration or system testing.

## When to run unit tests

* At the beginning of your coding session
* After you pull new/latest code from a repository
* After you've made any significant updates to your code
* Before you made a commit in Git
* Before you push your code to a repository
* Before you deploy your code

## What to unit test

- Testing that your code is handling things given expected input or situations is often called testing "happy" path
- Testing that your code can handle unexpected or aberrant input or situations is known as testing the "unhappy or sad" path
- You need to tests both paths

## What to unit test ?

- If this piece of code is provided with  “good” data does it process it as expected?
- If this piece of code is provided with malformed input does it handle it gracefully?
- How does it handle NULLs as input? The wrong data type?

## How much to unit test?

How much of your code to test is a tradeoff between the time/effort spent writing the tests and the reliability of your code.

"**Code coverage**" is the term used to denote how much of your code base is being tested. Typically teams will choose a specific percentage they are aiming for like 70% or 80%.

# Writing unit tests

## How to write a unit test

- Understand precisely what your function is supposed to do
- Define expected input
- Define expected output
- Create test data for expected input
- Create test data for corresponding expected output
- Execute target function/method/code using test data
- Assert that the function returns expected output

## How to write a unit test

- Note all possible unexpected situations cases (e.g. NULL input where a string was expected)
- Create test data for these cases
- Create test data for corresponding expected output
- Execute target function/method/code using test data
- Assert that the function returns expected output or handles unexpected input gracefully

## Tools for Python unit testing

* `unittest` - [Built in unit testing framework](https://docs.python.org/3/library/unittest.html)
* `pytest` - [Popular open source framework](https://docs.pytest.org)
