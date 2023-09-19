"""
Run tests for Ringling parameter sets
"""
# pylint: disable=duplicate-code
import os
import unittest

import requests

from test_utils import check_base_url

BASE_URL_KEY = "BASE_URL"

class ParameterSetsTests(unittest.TestCase):
    """
    Testing suite for parameter sets
    """
    def get_url(self):
        """
        Get the parameter set url
        :return: The full parameter sets url
        """
        return os.path.join(os.environ[BASE_URL_KEY], "v1/parameter_sets")

    def test_create_success(self):
        """
        Test if a parameter set can be created successfully
        :return: If a parameter set with correct schema can be successfully created
        """
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "is_active" : True }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)

    def test_create_bad_schema(self):
        """
        Test if a parameter set with a bad schema generates the correct response
        :return: If a parameter set with bad schema returns a 400 error
        """
        obj = { "this is a test" : 5,
                "and another test" : { "param1" : 1, "param2" : "2" },
                "test" : True }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 400)

    def test_list_params(self):
        """
        Test if displaying all parameter sets work correctly
        :return: If all parameter sets are created correctly, and returned in a list
        """
        param_ids = set()

        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "is_active" : True }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        param_ids.add(json_response["parameter_set_id"])

        obj = { "project_id" : 6,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "is_active" : True
        }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        param_ids.add(json_response["parameter_set_id"])

        obj = { "project_id" : 7,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "is_active" : False
        }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        param_ids.add(json_response["parameter_set_id"])

        response = requests.get(self.get_url(), timeout=5)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertIn("parameter_sets", json_response)

        observed_param_ids = {obj["parameter_set_id"] for obj in json_response["parameter_sets"]}

        # check that param_ids is a proper subset of observed_param_ids
        self.assertEqual(param_ids, observed_param_ids.intersection(param_ids))

    def test_get_by_id(self):
        """
        Test getting a parameter set by a specific ID
        :return: If getting a parameter set by ID was successful
        """
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "is_active" : False
        }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)

        url = os.path.join(self.get_url(), str(json_response["parameter_set_id"]))
        response = requests.get(url, timeout=5)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response2["parameter_set_id"], json_response["parameter_set_id"])
        self.assertEqual(obj["project_id"], json_response2["project_id"])
        self.assertEqual(obj["training_parameters"], json_response2["training_parameters"])
        self.assertEqual(obj["is_active"], json_response2["is_active"])

    def test_get_by_id_no_end(self):
        """
        Test getting a parameter set by a specific ID with a different activity status
        :return: If getting a parameter set by ID was successful
        """
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "is_active" : True
        }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)

        url = os.path.join(self.get_url(), str(json_response["parameter_set_id"]))
        response = requests.get(url, timeout=5)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response2["parameter_set_id"], json_response["parameter_set_id"])
        self.assertEqual(obj["project_id"], json_response2["project_id"])
        self.assertEqual(obj["training_parameters"], json_response2["training_parameters"])
        self.assertEqual(obj["is_active"], json_response2["is_active"])

    def test_get_by_bad_id(self):
        """
        Test getting a parameter set by a nonexistent ID
        :return: If getting a parameter set by a nonexistent ID returned a 404
        """
        param_id = 0

        url = os.path.join(self.get_url(), str(param_id))

        response = requests.get(url, timeout=5)
        self.assertEqual(response.status_code, 404)

        json_obj = response.json()
        self.assertIn("error", json_obj)

    def test_update_status(self):
        """
        Test updating the status of a parameter set
        :return: If updating a parameter set is successful
        """
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "is_active" : False
        }

        response = requests.post(self.get_url(),
                                 json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        url = os.path.join(self.get_url(),
                           str(json_response["parameter_set_id"]))

        update = { "is_active" : True }

        response = requests.patch(url, json=update, timeout=5)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response["parameter_set_id"], json_response2["parameter_set_id"])
        self.assertTrue(json_response2["is_active"])

        update = { "is_active" : False }

        response = requests.patch(url, json=update, timeout=5)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response["parameter_set_id"], json_response2["parameter_set_id"])
        self.assertFalse(json_response2["is_active"])

    def test_update_status_bad_schema(self):
        """
        Test updating the status of a parameter set with a bad schema
        :return: If updating a parameter set with a bad schema returns a 400
        """
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "is_active" : False
        }

        response = requests.post(self.get_url(),
                                 json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        url = os.path.join(self.get_url(),
                           str(json_response["parameter_set_id"]))

        update = { "this is a test" : True }

        response = requests.patch(url, json=update, timeout=5)

        self.assertEqual(response.status_code, 400)

    def test_update_status_bad_id(self):
        """
        Test updating a parameter set by a nonexistent ID
        :return: If patching a parameter set by a nonexistent ID returned a 404
        """
        param_id = 0

        url = os.path.join(self.get_url(),
                           str(param_id))

        update = {"is_active" : False }

        response = requests.patch(url, json=update, timeout=5)

        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    check_base_url(BASE_URL_KEY)
    unittest.main()
