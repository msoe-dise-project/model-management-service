import argparse
import datetime as dt
import os
import sys
import unittest

import requests

BASE_URL_KEY = "BASE_URL"

class ProjectsTests(unittest.TestCase):
    def get_url(self):
        return os.path.join(os.environ[BASE_URL_KEY], "v1/projects")

    def test_create(self):
        obj = { "project_name" : "test",
                "project_start" : dt.datetime.now().isoformat() }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        
        self.assertIn("project_id", json_response)
        self.assertIsInstance(json_response["project_id"], int)
        
    def test_create_no_name(self):
        obj = { "project_start" : dt.datetime.now().isoformat() }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 400)
        
    def test_create_no_start(self):
        obj = { "project_name" : "test" }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 400)
        
    def test_list_projects(self):
        response = requests.get(self.get_url())
        
        self.assertEqual(response.status_code, 200)
        
    def test_get_project(self):
        obj = { "project_name" : "test",
                "project_start" : dt.datetime.now().isoformat() }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)
        
        json_obj = response.json()
        self.assertIn("project_id", json_obj)
        project_id = json_obj["project_id"]
        self.assertIsInstance(project_id, int)

        url = os.path.join(self.get_url(),
                            str(project_id))
        response = requests.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        json_obj = response.json()
        self.assertIn("project_id", json_obj)
        self.assertIn("project_name", json_obj)
        self.assertIn("project_start", json_obj)
        self.assertIn("project_end", json_obj)
        
    def test_set_project_end_success(self):
        obj = { "project_name" : "test",
                "project_start" : dt.datetime.now().isoformat() }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)
        
        json_obj = response.json()
        self.assertIn("project_id", json_obj)
        project_id = json_obj["project_id"]
        self.assertIsInstance(project_id, int)
        
        project_update = { "project_end" : dt.datetime.now().isoformat() }

        url = os.path.join(self.get_url(), str(project_id), "project_end")
        response = requests.put(url,
                            json=project_update)
        
        self.assertEqual(response.status_code, 200)
        
        json_obj = response.json()
        self.assertIn("num_projects_updated", json_obj)
        self.assertEqual(json_obj["num_projects_updated"], 1)

if __name__ == "__main__":
    if BASE_URL_KEY not in os.environ:
        print("Must define the base URL using the {} environment variable".format(BASE_URL_KEY))
        sys.exit(1)

    unittest.main()
