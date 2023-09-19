"""
Run tests for Ringling model tests
"""
# pylint: disable=duplicate-code
import datetime as dt
import os
import unittest

import requests

from test_utils import check_base_url

BASE_URL_KEY = "BASE_URL"

class ModelTestsTests(unittest.TestCase):
    """
    Testing suite for model tests
    """
    def get_url(self):
        """
        Get the model test url
        :return: The full model tests url
        """
        return os.path.join(os.environ[BASE_URL_KEY], "v1/model_tests")

    def test_create_success(self):
        """
        Test if a model test can be created successfully
        :return: If a model test with correct schema can be successfully created
        """
        obj = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 2,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : { "recall" : 0.8, "precision" : 0.2 },
                "passed_testing" : True
              }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        self.assertIn("test_id", json_response)
        self.assertIsInstance(json_response["test_id"], int)

    def test_create_success_bad_schema(self):
        """
        Test if a model test with a bad schema generates the correct response
        :return: If a model test with bad schema returns a 400 error
        """
        obj = {
                "not_a_project_id" : 5,
                "bad parameters" : 1,
                "oops" : 2,
                "test_timestamp" : "today",
                "test_metrics" : { "recall" : 0.8, "precision" : 0.2 },
                "passed_testing" : None
              }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 400)

    def test_list_tests(self):
        """
        Test if displaying all model tests works correctly
        :return: If all model tests are created correctly, and returned in a list
        """
        obj1 = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 2,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : { "recall" : 0.8, "precision" : 0.2 },
                "passed_testing" : True
              }

        response = requests.post(self.get_url(),
                            json=obj1, timeout=5)

        self.assertEqual(response.status_code, 201)

        obj2 = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 3,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : { "recall" : 0.8, "precision" : 0.2 },
                "passed_testing" : True
              }

        response = requests.post(self.get_url(),
                            json=obj2, timeout=5)

        self.assertEqual(response.status_code, 201)

        obj3 = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 53,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : { "recall" : 0.8, "precision" : 0.2 },
                "passed_testing" : True
              }

        response = requests.post(self.get_url(),
                            json=obj3, timeout=5)

        self.assertEqual(response.status_code, 201)

        response = requests.get(self.get_url(), timeout=5)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertIn("model_tests", json_response)
        self.assertGreaterEqual(len(json_response["model_tests"]), 3)

    def test_get_test_by_id(self):
        """
        Test getting a model test by a specific ID
        :return: If getting a model by ID was successful
        """
        obj1 = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 2,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : { "recall" : 0.8, "precision" : 0.2 },
                "passed_testing" : True
              }

        response = requests.post(self.get_url(),
                            json=obj1, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        model_id = json_response["test_id"]

        url = os.path.join(self.get_url(), str(model_id))
        response = requests.get(url, timeout=5)

        self.assertEqual(response.status_code, 200)

    def test_get_test_by_bad_id(self):
        """
        Test getting a model by a nonexistent ID
        :return: If getting a model test by a nonexistent ID returned a 404
        """
        test_id = 0

        url = os.path.join(self.get_url(), str(test_id))

        response = requests.get(url, timeout=5)
        self.assertEqual(response.status_code, 404)

        json_obj = response.json()
        self.assertIn("error", json_obj)

if __name__ == "__main__":
    check_base_url(BASE_URL_KEY)
    unittest.main()
