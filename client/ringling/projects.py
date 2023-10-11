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
from ringling_lib.project import Project
from ringling_lib.ringling_db import RinglingDBSession
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


def create_project(session, project_name, metadata):
    """
    Create a project on the Ringling service
    :param session: An instance of Ringling DB session
    :param project_name: The name of the project to create
    :return: The response from the service
    """
    proj = Project(project_name, metadata)
    return session.create_project(proj)


def list_projects(session):
    """
    List all the projects in the Ringling Service
    :param session: An instance of Ringling DB session
    :return: None
    """
    pprint.pprint(session.list_projects_json())


def get_project(session, project_id):
    """
    Return information about a specific project in the Ringling Service by ID
    :param session: An instance of Ringling DB session
    :param project_id:
    :return: None
    """
    pprint.pprint(session.get_project_json(project_id))
