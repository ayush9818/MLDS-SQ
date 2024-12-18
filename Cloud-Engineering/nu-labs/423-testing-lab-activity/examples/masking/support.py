"""
Script

The script below parses customer support tickets of the form (ticket_id, user_id, body) 

"""

import logging
import re

logger = logging.getLogger(__name__)

PHONE_REGEX = r"\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*"
PHONE_PATTERN = re.compile(PHONE_REGEX)
REPLACEMENT = " xxxxxxxxxx "


def mask_phone_numbers(body, pattern=PHONE_PATTERN):
    try:
        masked = pattern.sub(REPLACEMENT, body)
    except TypeError:
        logger.error("A string was not provided for `body`")
        raise TypeError("A string must be provided for `body`.")
    except AttributeError:
        logger.error("A re.compile object must be provided for `pattern`.")
        raise AttributeError("A re.compile object must be provided for `pattern`.")
    except Exception as e:
        logger.error("String was not able to be masked due to the exception: %s", e)
        raise e
    return masked
