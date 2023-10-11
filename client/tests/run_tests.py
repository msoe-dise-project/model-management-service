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
from tests.test_connection import TestConnection
from tests.test_projects import TestProjects
from tests.test_parameter_sets import TestParameterSets
from tests.test_trained_models import TestTrainedModels
from tests.test_model_tests import TestModelTests

test_suite = unittest.TestSuite()

# Add additional tests here
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestConnection))
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestProjects))
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestParameterSets))
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestTrainedModels))
test_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestModelTests))

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite)
