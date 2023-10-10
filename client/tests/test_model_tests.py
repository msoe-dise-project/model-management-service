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
from datetime import datetime

from ringling_lib.model_test import ModelTest
from ringling_lib.ringling_db import RinglingDBSession

BASE_URL_KEY = "RINGLING_BASE_URL"
base_url = os.environ.get(BASE_URL_KEY)

class TestModelTests(unittest.TestCase):
    """
    Test interacting with Model Tests
    """
    def test_model_test_create_dict(self):
        """
        Create a model test using dictionary values
        :return: If the model test was created successfully
        """
        session = RinglingDBSession(base_url)
        obj = {"project_id": 3,
                "parameter_set_id": 2,
                "model_id": 4,
                "test_timestamp": datetime.now().isoformat(),
                "test_metrics": {"AUROC": 0.95},
                "passed_testing": True,
                "metadata": {"test data": "important test data"}}
        test_model_test = ModelTest(
                obj['project_id'],
                obj['parameter_set_id'],
                obj['model_id'],
                obj['test_timestamp'],
                obj['test_metrics'],
                obj['passed_testing'],
                obj['metadata']
        )
        model_test_id = session.create_model_test(test_model_test)
        self.assertIsInstance(model_test_id, int)

    def test_model_test_create_direct(self):
        """
        Create a model test using direct values
        :return: If the model test was created successfully
        """
        session = RinglingDBSession(base_url)
        test_model_test = ModelTest(
        5, 4, 7, datetime.now().isoformat(),
        {"AUROC": 0.95}, True, {"test data": "important test data"}
        )
        model_test_id = session.create_model_test(test_model_test)
        self.assertIsInstance(model_test_id, int)

    def test_model_test_get(self):
        """
        Get a model test given an ID
        :return: If the retrieved model test metadata and test timestamp match the ones sent
        """
        session = RinglingDBSession(base_url)
        test_model_test = ModelTest(
        5, 4, 7, datetime.now().isoformat(),
        {"AUROC": 0.97}, True, {"stored test data": "very important test data"}
        )
        model_test_id = session.create_model_test(test_model_test)
        returned_model_test = session.get_model_test(model_test_id)
        self.assertEqual(test_model_test.test_timestamp, returned_model_test.test_timestamp)
        self.assertEqual(test_model_test.metadata, returned_model_test.metadata)

    def test_model_test_list(self):
        """
        Test listing trained models sets
        :return: If the returned trained models contain the newly created ones
        """
        session = RinglingDBSession(base_url)
        test_model_test = ModelTest(
        5, 5, 7, datetime.now().isoformat(),
        {"AUROC": 0.95}, False, {"test data": "important test data"}
        )
        test_model_test_2 = ModelTest(
        5, 6, 8, datetime.now().isoformat(),
        {"AUROC": 0.97}, True, {"test data": "data 2"}
        )
        test_model_test_3 = ModelTest(
        5, 7, 9, datetime.now().isoformat(),
        {"AUROC": 0.98}, True, {"test data": "data 3"}
        )
        model_test_id = session.create_model_test(test_model_test)
        model_test_id_2 = session.create_model_test(test_model_test_2)
        model_test_id_3 = session.create_model_test(test_model_test_3)

        model_tests = session.list_model_tests()

        self.assertTrue(model_test_id in model_tests)
        self.assertTrue(model_test_id_2 in model_tests)
        self.assertTrue(model_test_id_3 in model_tests)