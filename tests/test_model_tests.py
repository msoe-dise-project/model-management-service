import argparse
import datetime as dt
import json
import os
import sys
import unittest

import requests

BASE_URL_KEY = "BASE_URL"

class ModelTestsTests(unittest.TestCase):
    def get_url(self):
        return os.path.join(os.environ[BASE_URL_KEY], "v1/model_tests")

    def test_create_success(self):
        test_model = set([1, 3, 5])
        
        obj = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 2,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : json.dumps({ "recall" : 0.8, "precision" : 0.2 }),
                "passed_testing" : True
              }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        self.assertIn("test_id", json_response)
        self.assertIsInstance(json_response["test_id"], int)
        
    def test_list_tests(self):
        obj1 = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 2,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : json.dumps({ "recall" : 0.8, "precision" : 0.2 }),
                "passed_testing" : True
              }
                 
        response = requests.post(self.get_url(),
                            json=obj1)

        self.assertEqual(response.status_code, 200)

        obj2 = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 3,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : json.dumps({ "recall" : 0.8, "precision" : 0.2 }),
                "passed_testing" : True
              }

        response = requests.post(self.get_url(),
                            json=obj2)

        self.assertEqual(response.status_code, 200)

        obj3 = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 53,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : json.dumps({ "recall" : 0.8, "precision" : 0.2 }),
                "passed_testing" : True
              }
                 
        response = requests.post(self.get_url(),
                            json=obj3)

        self.assertEqual(response.status_code, 200)

        response = requests.get(self.get_url())
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertIn("model_tests", json_response)
        self.assertGreaterEqual(len(json_response["model_tests"]), 3)
        
    def test_get_test_by_id(self):
        obj1 = {
                "project_id" : 5,
                "parameter_set_id" : 1,
                "model_id" : 2,
                "test_timestamp" : dt.datetime.now().isoformat(),
                "test_metrics" : json.dumps({ "recall" : 0.8, "precision" : 0.2 }),
                "passed_testing" : True
              }

        response = requests.post(self.get_url(),
                            json=obj1)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        model_id = json_response["test_id"]
        
        url = os.path.join(self.get_url(), str(model_id))
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    if BASE_URL_KEY not in os.environ:
        print("Must define the base URL using the {} environment variable".format(BASE_URL_KEY))
        sys.exit(1)

    unittest.main()
