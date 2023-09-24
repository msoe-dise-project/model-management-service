"""
Run tests for Ringling projects
"""
# pylint: disable=duplicate-code
import os
import unittest

import requests

from test_utils import check_base_url

BASE_URL_KEY = "BASE_URL"

class ProjectsTests(unittest.TestCase):
    """
    Testing suite for projects
    """
    def get_url(self):
        """
        Get the project url
        :return: The full project url
        """
        return os.path.join(os.environ[BASE_URL_KEY], "v1/projects")

    def test_create(self):
        """
        Test if a project can be created successfully
        :return: If a project with the correct schema can be successfully created
        """
        obj = { "project_name" : "test",
                "metadata": {"meta1": 1, "meta2": 2}
                }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        self.assertIn("project_id", json_response)
        self.assertIsInstance(json_response["project_id"], int)

    def test_create_invalid_object(self):
        """
        Test if a project with a bad schema generates the correct response
        :return: If a project with a bad schema returns a 400 error
        """
        obj = { "this is a test" : "test",
                "metadata": {"meta1": 1, "meta2": 2}
                }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 400)

    def test_list_projects(self):
        """
        Test if displaying all project work correctly
        :return: If all projects are created correctly, and returned in a list
        """
        response = requests.get(self.get_url(), timeout=5)

        self.assertEqual(response.status_code, 200)

    def test_get_project(self):
        """
        Test getting a project by a specific ID
        :return: If getting a project by ID was successful
        """
        obj = { "project_name" : "test2",
                "metadata": {"meta1": 1, "meta2": 2}
                }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)

        self.assertEqual(response.status_code, 201)

        json_obj = response.json()
        self.assertIn("project_id", json_obj)
        project_id = json_obj["project_id"]
        self.assertIsInstance(project_id, int)

        url = os.path.join(self.get_url(),
                            str(project_id))
        response = requests.get(url, timeout=5)

        self.assertEqual(response.status_code, 200)

        json_obj = response.json()
        self.assertIn("project_id", json_obj)
        self.assertIn("project_name", json_obj)

    def test_get_project_bad_id(self):
        """
        Test getting a project by a nonexistent ID
        :return: If getting a project by a nonexistent ID returned a 404
        """
        project_id = 0

        url = os.path.join(self.get_url(), str(project_id))

        response = requests.get(url, timeout=5)
        self.assertEqual(response.status_code, 404)

        json_obj = response.json()
        self.assertIn("error", json_obj)

    def test_get_project_bad_name(self):
        """
        Test creating a project with an existing name
        :return: If creating a project by an already existing name returns a 400
        """
        obj = { "project_name" : "test",
                "metadata": {"meta1": 1, "meta2": 2}
                }

        response = requests.post(self.get_url(),
                            json=obj, timeout=5)
        self.assertEqual(response.status_code, 400)

        json_obj = response.json()
        self.assertIn("error", json_obj)

if __name__ == "__main__":
    check_base_url(BASE_URL_KEY)
    unittest.main()
