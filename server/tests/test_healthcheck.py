import argparse
import datetime as dt
import os
import sys
import unittest

import requests

BASE_URL_KEY = "BASE_URL"

class ProjectsTests(unittest.TestCase):
    def get_url(self):
        return os.path.join(os.environ[BASE_URL_KEY], "healthcheck")

    def test_healthcheck(self):
        response = requests.get(self.get_url())
        
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    if BASE_URL_KEY not in os.environ:
        print("Must define the base URL using the {} environment variable".format(BASE_URL_KEY))
        sys.exit(1)

    unittest.main()
