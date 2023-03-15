import argparse
import datetime as dt
import json
import os
import sys
import unittest

import requests

BASE_URL_KEY = "BASE_URL"

class ParameterSetsTests(unittest.TestCase):
    def get_url(self):
        return os.path.join(os.environ[BASE_URL_KEY], "v1/parameter_sets")

    def test_create_success(self):
        obj = { "project_id" : 5,
                "training_parameters" : json.dumps({ "param1" : 1, "param2" : "2" }),
                "is_active" : True }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)
        
    def test_create_bad_schema(self):
        obj = { "this is a test" : 5,
                "and another test" : json.dumps({ "param1" : 1, "param2" : "2" }),
                "test" : True }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 400)
        
    def test_list_params(self):
        param_ids = set()
        
        obj = { "project_id" : 5,
                "training_parameters" : json.dumps({ "param1" : 1, "param2" : "2" }),
                "is_active" : True }
                
        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        param_ids.add(json_response["parameter_set_id"])
                
        obj = { "project_id" : 6,
                "training_parameters" : json.dumps({ "param1" : 1, "param2" : "2" }),
                "is_active" : True
        }
                
        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        param_ids.add(json_response["parameter_set_id"])
                
        obj = { "project_id" : 7,
                "training_parameters" : json.dumps({ "param1" : 1, "param2" : "2" }),
                "is_active" : False
        }
                
        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        param_ids.add(json_response["parameter_set_id"])

        response = requests.get(self.get_url())

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertIn("parameter_sets", json_response)
        
        observed_param_ids = set([obj["parameter_set_id"] for obj in json_response["parameter_sets"]])
        
        # check that param_ids is a proper subset of observed_param_ids
        self.assertEqual(param_ids, observed_param_ids.intersection(param_ids))
    
    def test_get_by_id(self):
        obj = { "project_id" : 5,
                "training_parameters" : json.dumps({ "param1" : 1, "param2" : "2" }),
                "is_active" : False
        }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)

        url = os.path.join(self.get_url(), str(json_response["parameter_set_id"]))
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response2["parameter_set_id"], json_response["parameter_set_id"])
        self.assertEqual(obj["project_id"], json_response2["project_id"])
        self.assertEqual(obj["training_parameters"], json_response2["training_parameters"])
        self.assertEqual(obj["is_active"], json_response2["is_active"])
        
    def test_get_by_id_no_end(self):
        obj = { "project_id" : 5,
                "training_parameters" : json.dumps({ "param1" : 1, "param2" : "2" }),
                "is_active" : True
        }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)

        url = os.path.join(self.get_url(), str(json_response["parameter_set_id"]))
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response2["parameter_set_id"], json_response["parameter_set_id"])
        self.assertEqual(obj["project_id"], json_response2["project_id"])
        self.assertEqual(obj["training_parameters"], json_response2["training_parameters"])
        self.assertEqual(obj["is_active"], json_response2["is_active"])
        
    def test_update_status(self):
        obj = { "project_id" : 5,
                "training_parameters" : json.dumps({ "param1" : 1, "param2" : "2" }),
                "is_active" : False
        }

        response = requests.post(self.get_url(),
                                 json=obj)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        url = os.path.join(self.get_url(),
                           str(json_response["parameter_set_id"]))
        
        update = { "is_active" : True }
        
        response = requests.patch(url, json=update)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response["parameter_set_id"], json_response2["parameter_set_id"])
        self.assertTrue(json_response2["is_active"])
        
        update = { "is_active" : False }
        
        response = requests.patch(url, json=update)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response["parameter_set_id"], json_response2["parameter_set_id"])
        self.assertFalse(json_response2["is_active"])
        
    def test_update_status_bad_schema(self):
        obj = { "project_id" : 5,
                "training_parameters" : json.dumps({ "param1" : 1, "param2" : "2" }),
                "is_active" : False
        }

        response = requests.post(self.get_url(),
                                 json=obj)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        url = os.path.join(self.get_url(),
                           str(json_response["parameter_set_id"]))
        
        update = { "this is a test" : True }
        
        response = requests.patch(url, json=update)

        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    if BASE_URL_KEY not in os.environ:
        print("Must define the base URL using the {} environment variable".format(BASE_URL_KEY))
        sys.exit(1)

    unittest.main()
