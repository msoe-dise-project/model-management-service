"""
Commonly used methods for testing
"""
import os
import sys


def check_base_url(base_url_key):
    """
    Check if the base url is an environment variable
    :param BASE_URL_KEY: The key for the base url variable
    """
    if base_url_key not in os.environ:
        print(f"Must define the base URL using the {base_url_key} environment variable")
        sys.exit(1)
