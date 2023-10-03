"""
Copyright 2023 MSOE DISE Project
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import unittest
from requests.exceptions import ConnectTimeout
from ringling_lib.ringling_db import RinglingDBSession

BASE_URL_KEY = "RINGLING_BASE_URL"
base_url = os.environ.get(BASE_URL_KEY)
class TestConnection(unittest.TestCase):
    """
    Test the connection to the Ringling service
    """
    def test_connection_good_url(self):
        """
        Test if the connection works with the correct URL
        :return: If the connection is healthy
        """
        test_session = RinglingDBSession(base_url)
        self.assertTrue(test_session.perform_connect_check())

    def test_session_bad_url(self):
        """
        Test if the connection fails correctly with a bad url
        :return: If the bad url failed to connect
        """
        test_session = RinglingDBSession("http://localhost:80")
        self.assertFalse(test_session.perform_connect_check())