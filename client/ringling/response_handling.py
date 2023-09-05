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

import sys
import pprint
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError


def handle_create(response):
    """
    Handle the response from create commands
    :param response: the response object
    :return: if the response was a success
    """
    if 200 <= response.status_code < 300:
        return True
    if response.status_code == 400:
        print(response.json()['error'], file=sys.stderr)
        sys.exit(1)
    if response.status_code == 403:
        print("Connection forbidden. "
              "Is there another service such as a Jupyter Notebook running on this port?")
        sys.exit(1)
    return False


def handle_modify(response, object_type, cur_id):
    """
    Handle the response from modify commands
    :param response: the response object
    :param object_type: the object type (for displaying errors)
    :param cur_id: the id of the object
    :return: if the response was a success
    """
    if 200 <= response.status_code < 300:
        return True
    if response.status_code == 404:
        print(f"Invalid {object_type} ID {cur_id}", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 400:
        print(response.json()['error'], file=sys.stderr)
        sys.exit(1)
    if response.status_code == 403:
        print("Connection forbidden. "
              "Is there another service such as a Jupyter Notebook running on this port?")
        sys.exit(1)
    return False


def handle_get(response, object_type, cur_id):
    """
    Handle the response from get commands
    :param response: the response object
    :param object_type: the object type (for displaying errors)
    :param cur_id: the id of the object
    :return: if the response was a success
    """
    if 200 <= response.status_code < 300:
        response_json = response.json()
        pprint.pprint(response_json)
    if response.status_code == 404:
        print(f"Invalid {object_type} ID {cur_id}", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 403:
        print("Connection forbidden. "
              "Is there another service such as a Jupyter Notebook running on this port?")
        sys.exit(1)


def perform_list(rest_url):
    """
    Get the list from the REST url
    :param rest_url: The url to perform GET on
    :return: None
    """
    try:
        response = requests.get(rest_url, timeout=5)
        if response.status_code == 403:
            print("Connection forbidden. "
                  "Is there another service such as a Jupyter Notebook running on this port?")
            sys.exit(1)
        response_json = response.json()
        pprint.pprint(response_json)
    except RequestsConnectionError:
        connection_error()


def connection_error():
    """
    To be called when there is any type of connection error
    :return: None
    """
    print("Can not connect to model management service. Is the Ringling server running?", file=sys.stderr)
    sys.exit(1)
