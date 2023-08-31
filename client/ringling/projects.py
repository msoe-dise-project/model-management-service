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

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from .response_handling import handle_create
from .response_handling import handle_get
from .response_handling import perform_list
from .response_handling import connection_error


def get_url(base_url):
    """
    Get the URL for interacting with projects
    :return: The project URL
    """
    return base_url + "/v1/projects"


def create_project(base_url, project_name):
    """
    Create a project on the Ringling service
    :param base_url: The URL of the Ringling Service
    :param project_name: The name of the project to create
    :return: The response from the service
    """
    obj = {"project_name": project_name}
    try:
        response = requests.post(get_url(base_url),
                                 json=obj, timeout=5)
        if handle_create(response):
            print(f"Project {project_name} created successfully")
            print("Project ID:", response.json()['project_id'])
    except RequestsConnectionError:
        connection_error()


def list_projects(base_url):
    """
    List all the projects in the Ringling Service
    :param base_url: The URL of the Ringling Service
    :return: None
    """
    perform_list(get_url(base_url))


def get_project(base_url, project_id):
    """
    Return information about a specific project in the Ringling Service by ID
    :param base_url: The URL of the Ringling Service
    :param project_id:
    :return: None
    """
    url = get_url(base_url) + "/" + str(project_id)
    try:
        response = requests.get(url, timeout=5)
        handle_get(response, "Project", project_id)
    except RequestsConnectionError:
        connection_error()
