import pytest
import support


def test_mask_phone_numbers_1():
    # Test expected input
    message = "my phone number is 1-123-456-7890"
    assert support.mask_phone_numbers(message) == "my phone number is xxxxxxxxxx "


def test_mask_phone_numbers_multiple():
    # Test multiple
    message = "1-123-456-7890 and 1-123-456-7890"
    assert support.mask_phone_numbers(message) == " xxxxxxxxxx and xxxxxxxxxx "


def test_mask_phone_numbers_no_match():
    # No match
    message = "My app is broken!"
    assert support.mask_phone_numbers(message) == "My app is broken!"


def test_mask_phone_numbers_empty_msg():
    # Empty string
    message = ""
    assert support.mask_phone_numbers(message) == ""


def test_mask_phone_numbers_none():
    # None should result in a type error
    message = None
    with pytest.raises(TypeError):
        support.mask_phone_numbers(message)


def test_mask_phone_numbers_bad_pattern():
    # A pattern that isn't a re.compile object should result in an attribute error
    message = "my phone number is 1-123-456-7890"
    pattern = "PATTERN"
    with pytest.raises(AttributeError):
        support.mask_phone_numbers(message, pattern)
