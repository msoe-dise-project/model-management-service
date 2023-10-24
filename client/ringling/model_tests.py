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
import pprint

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from ringling_lib.model_test import ModelTest
from ringling_lib.ringling_db import RinglingDBSession
from .response_handling import handle_create
from .response_handling import handle_get
from .response_handling import perform_list
from .response_handling import connection_error

def create_model_test(session, obj):
    """
    Create a model test on the Ringling service
    :param session: An instance of a Ringling DB session
    :param obj: The model object payload
    :return: None
    """
    cur_id = session.create_model_test(obj)
    print(f"Model Test created with ID {cur_id}")


def get_model_test(session, model_test_id):
    """
    Get a model test given an ID
    :param session: An instance of a Ringling DB session
    :param model_test_id: The ID of the model test
    :return: None
    """
    pprint.pprint(session.get_model_test_json(model_test_id))


def list_model_tests(session):
    """
    List all the model tests in the Ringling Service
    :param session: An instance of a Ringling DB session
    :return: None
    """
    pprint.pprint(session.list_model_tests_json())
