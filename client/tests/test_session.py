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

import unittest
from requests.exceptions import ConnectTimeout
from ringling_lib.session import Session

class TestSession(unittest.TestCase):

    def test_connection_env_url(self):
        test_session = Session()
        self.assertTrue(test_session.perform_connect_check())

    def test_connection_good_url(self):
        test_session = Session("http://localhost:8888")
        self.assertTrue(test_session.perform_connect_check())

    def test_session_bad_url(self):
        test_session = Session("http://localhost:1111")
        with self.assertRaises(ConnectTimeout):
            test_session.perform_connect_check()


