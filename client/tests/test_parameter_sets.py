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

from ringling_lib.param_set import ParameterSet
from ringling_lib.ringling_db import RinglingDBSession

BASE_URL_KEY = "RINGLING_BASE_URL"
base_url = os.environ.get(BASE_URL_KEY)

class TestParameterSets(unittest.TestCase):
    """
    Test interacting with Parameter Sets
    """
    def test_param_create_dict(self):
        """
        Create a parameter set using dictionary values
        :return: If the parameter set was created successfully
        """
        session = RinglingDBSession(base_url)
        obj = { "project_id" : 2,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "is_active" : False,
                "metadata": {"meta1": 1, "meta2": 2}
        }
        test_param_set = ParameterSet(
            obj['project_id'],
            obj['training_parameters'],
            obj['is_active'],
            obj['metadata']
        )
        param_set_id = session.create_param_set(test_param_set)
        self.assertIsInstance(param_set_id, int)

    def test_param_create_direct(self):
        """
        Create a parameter set using direct values
        :return: If the parameter set was created successfully
        """
        session = RinglingDBSession(base_url)
        test_param_set = ParameterSet(
            3, { "param1" : 1, "param2" : "2" },
            False, {"meta1": 1, "meta2": 2}
        )
        param_set_id = session.create_param_set(test_param_set)
        self.assertIsInstance(param_set_id, int)

    def test_param_get(self):
        """
        Get a parameter set given an ID
        :return: If the retrieved parameter set parameters match the ones sent
        """
        session = RinglingDBSession(base_url)
        test_param_set = ParameterSet(
            4, { "param1" : 5, "param2" : "6" },
            False, {"meta4": 1, "meta5": 90}
        )
        param_set_id = session.create_param_set(test_param_set)
        returned_param_set = session.get_param_set(param_set_id)
        self.assertEqual(test_param_set.training_parameters, returned_param_set.training_parameters)