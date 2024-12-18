# test_date_calculations.py

import pytest
from datetime import date, timedelta

# Function to be tested
def add_days(start_date, num_days):
    return start_date + timedelta(days=num_days)

# Unit test
def test_add_days():
    start_date = date(2023, 1, 1)
    result = add_days(start_date, 5)
    assert result == date(2023, 1, 6)

# Fixture
@pytest.fixture
def setup_dates():
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 10)
    return start_date, end_date

# Parameterized test using fixture
@pytest.mark.parametrize("num_days, expected_date", [
    (1, date(2023, 1, 2)),
    (7, date(2023, 1, 8)),
    (10, date(2023, 1, 11))
])
def test_add_days_with_fixture(setup_dates, num_days, expected_date):
    start_date, _ = setup_dates
    result = add_days(start_date, num_days)
    assert result == expected_date
