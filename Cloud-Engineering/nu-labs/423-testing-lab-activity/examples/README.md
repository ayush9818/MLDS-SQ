# Testing examples

# Phone number masking 

You are using customer support ticket data to understand and address the customer issues but first you need to cleanse the data of sensitive information, specifically phone numbers.

* `support.py` has a single function that masks phone numbers
* `test_support.py` is the unit test file

## Test cases in test file

* Expected input (phone number)
* Multiple phone numbers in text
* No phone number
* Empty string 
* (commented out) `None` input

## Build Docker image for testing

* Got to the `masking` directory: `cd ./masking`
* Build the docker image: `docker build -t test_masking .`

## Run pytest using container

Run pytest: `docker run test_masking` 

## Testing "unhappy" path

* In `test_support.py` uncomment the final unit test 
* Re-build the docker image: `docker build -t test_masking .`
* Run pytest again: `docker run test_masking` 



# Aquastat helper

You are analysing data to understand the impact of rainfall on GDP across geographies. 

* `aquastat_helper.py` contains helper functions for slicing data across time frame, country, and variable
* `test_aquastat_helper.py` is the unit test file

## Test cases in test file

* Valid time frame
* Invalid time frame returning empty set
* Valid country 
* Invalid country returning empty set
* Valid variable
* Invalid variable returning empty set
* Empty variable input returning empty set

## Build Docker image for testing

* Got to the `aquastat` directory: `cd ./aquastat`
* Build the docker image: `docker build -t test_aqua .`

## Run pytest using container

Run pytest: `docker run test_aqua` 




