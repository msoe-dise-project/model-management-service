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

from ringling_lib.project import Project
from ringling_lib.ringling_db import RinglingDBSession

BASE_URL_KEY = "RINGLING_BASE_URL"
base_url = os.environ.get(BASE_URL_KEY)


class TestProjects(unittest.TestCase):
    """
    Test interacting with Projects
    """
    def test_project_create_dict(self):
        """
        Create a project using dictionary values
        :return: If the project was created successfully
        """
        session = RinglingDBSession(base_url)
        obj = {"project_name": "test10",
               "metadata": {"val10": 1, "val2": "2"}}
        test_project = Project(obj["project_name"], obj["metadata"])
        project_id = session.create_project(test_project)
        self.assertIsInstance(project_id, int)

    def test_project_create_direct(self):
        """
        Create a project using direct values
        :return: IF the project was created successfully
        """
        session = RinglingDBSession(base_url)
        test_project = Project("test20", {"val1": 1, "val2": "2"})
        project_id = session.create_project(test_project)
        self.assertIsInstance(project_id, int)

    def test_project_create_bad_name(self):
        """
        Create a project using an existing name
        :return: If the duplicate name project failed to be created
        """
        session = RinglingDBSession(base_url)
        test_project = Project("test30", {"val1": 1, "val2": "2"})
        session.create_project(test_project)
        bad_project = session.create_project(test_project)
        self.assertEqual(bad_project, None)

    def test_project_get(self):
        """
        Test getting a project given an ID
        :return: If the retrieved project name matches the one sent
        """
        session = RinglingDBSession(base_url)
        test_project = Project("test40", {"val2": 2, "val3": "3"})
        project_id = session.create_project(test_project)
        returned_project = session.get_project(project_id)
        self.assertEqual(test_project.project_name, returned_project.project_name)

    def test_project_list(self):
        """
        Test listing projects
        :return: If the returned projects contain the newly created ones
        """
        session = RinglingDBSession(base_url)
        test_project = Project("test_list1", {"val2": 2, "val3": "3"})
        test_project_2 = Project("test_list2", {"val2": 2, "val3": "3"})
        test_project_3 = Project("test_list3", {"val2": 2, "val3": "3"})
        project_id = session.create_project(test_project)
        project_id_2 = session.create_project(test_project_2)
        project_id_3 = session.create_project(test_project_3)
        projects = session.list_projects()

        self.assertTrue(project_id in projects)
        self.assertTrue(project_id_2 in projects)
        self.assertTrue(project_id_3 in projects)
