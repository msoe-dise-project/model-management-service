"""
Run tests for the healthcheck service
"""
import os
import sys
import unittest

import requests

BASE_URL_KEY = "BASE_URL"

from test_utils import check_base_url

class HealthcheckTests(unittest.TestCase):
    """
    Contains all tests pertaining to healthcheck service
    """
    def get_url(self):
        """
        Get the URL
        :return: The healthcheck URL
        """
        return os.path.join(os.environ[BASE_URL_KEY], "healthcheck")

    def test_healthcheck(self):
        """
        Make sure the healthcheck is working correctly
        :return: Healthcheck passed
        """
        response = requests.get(self.get_url(), timeout=5)

        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    check_base_url(BASE_URL_KEY)
    unittest.main()
