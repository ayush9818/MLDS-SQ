import os
from typing import Optional

import requests

URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(
    city: str, mode: str = "json", units: Optional[str] = None
) -> tuple[bool, str]:
    """Fetch weather data from the OpenWeather API

    :param city: name of the city for which to query weather
    :param mode: should be one of "json", "xml", defaults to "json"
    :param units: imperial or metric units for weather, defaults to None
    :raises ValueError: if invalid mode is passed
    :return: true/false if response is okay, content of response
    :rtype: tuple[bool, str]
    """
    # TODO: Implement this function
    return True, "NOT YET IMPLEMENTED"


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("WEATHER FOR CHICAGO")
    print("=" * 60)
    okay, result = get_weather("Chicago")
    if not okay:
        print("Request for Chicago weather failed")
    print(result)

    print("\n" + "=" * 60)
    print("XML FORMAT")
    print("=" * 60)
    # TODO: Make appropriate request and print response

    print("\n" + "=" * 60)
    print("METRIC UNITS")
    print("=" * 60)
    # TODO: Make appropriate request and print response
