"""
Commonly used methods for testing
"""
import os
import sys


def check_base_url(BASE_URL_KEY):
    """
    Check if the base url is an environment variable
    :param BASE_URL_KEY: The key for the base url variable
    """
    if BASE_URL_KEY not in os.environ:
        print(f"Must define the base URL using the {BASE_URL_KEY} environment variable")
        sys.exit(1)

