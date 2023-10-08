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
from .project import Project
from .param_set import ParameterSet
from .trained_model import TrainedModel
from .model_test import ModelTest
from .response_handling import handle_create
from .response_handling import handle_get
from .response_handling import perform_list
from .response_handling import connection_error


def json_to_project(project_json, id_tuple=False):
    """
    Convert a dictionary to a project
    :param project_json: A dictionary containing the project data
    :param id_tuple: Whether to include the id
    :return: a Project object
    """

    project_obj = Project(
        project_json['project_name'],
        project_json['metadata']
    )
    if id_tuple:
        return project_json['project_id'], project_obj
    return project_obj


def json_to_param_set(param_set_json, id_tuple=False):
    """
    Convert a dictionary to a parameter set
    :param param_set_json: A dictionary containing the parameter set
    :param id_tuple: Whether to include the id
    :return: a ParameterSet object
    """
    param_set_obj = ParameterSet(
        param_set_json['project_id'],
        param_set_json['training_parameters'],
        param_set_json['is_active'],
        param_set_json['metadata']
    )
    if id_tuple:
        return param_set_json['parameter_set_id'], param_set_obj
    return param_set_obj


def json_to_trained_model(trained_model_json, id_tuple=False):
    """
    Convert a dictionary to a trained model
    :param trained_model_json: A dictionary containing the trained model information
    :param id_tuple: Whether to include the id
    :return: a TrainedModel object
    """
    trained_model_obj = TrainedModel(
        trained_model_json['project_id'],
        trained_model_json['parameter_set_id'],
        trained_model_json['training_data_from'],
        trained_model_json['training_data_until'],
        trained_model_json['model_object'],
        trained_model_json['train_timestamp'],
        trained_model_json['deployment_stage'],
        trained_model_json['backtest_timestamp'],
        trained_model_json['backtest_metrics'],
        trained_model_json['passed_backtesting'],
        trained_model_json['metadata']
    )
    if id_tuple:
        return trained_model_json['model_id'], trained_model_obj
    return trained_model_obj


def json_to_model_test(model_test_json, id_tuple=False):
    """
    Convert a dictionary to a model test
    :param model_test_json: A dictionary containing the model test information
    :param id_tuple: Whether to include the id
    :return: a ModelTest object
    """
    model_test_obj = ModelTest(
        model_test_json['project_id'],
        model_test_json['parameter_set_id'],
        model_test_json['model_id'],
        model_test_json['test_timestamp'],
        model_test_json['test_metrics'],
        model_test_json['passed_testing'],
        model_test_json['metadata']
    )
    if id_tuple:
        return model_test_json['test_id'], model_test_obj
    return model_test_obj


def obj_list(cur_url, obj_func):
    """
    General helper function for listing resources
    :param cur_url: The url to list from
    :param obj_func: The conversion function
    :return: A dictionary of type id:object
    """
    object_json = perform_list(cur_url)
    object_list = [obj_func(obj, True) for obj in object_json]
    return dict(object_list)

class RinglingDBSession:
    """
    Main object to interact with Ringling
    """

    def __init__(self, url):
        """
        Initialize ringling
        :param url: the url for the main Ringling process
        """
        self.url = url
        self.project_url = url + "/v1/projects"
        self.param_url = url + "/v1/parameter_sets"
        self.trained_model_url = url + "/v1/trained_models"
        self.model_test_url = url + "/v1/model_tests"

    def perform_connect_check(self):
        """
        Check if healthcheck returns that Ringling is healthy
        :return: If the database connection is healthy
        """
        try:
            response = requests.get(self.url + "/healthcheck", timeout=0.5)
            response_json = response.json()
            return bool(response_json["database"]["connection"]["healthy"])
        except requests.exceptions.ConnectTimeout:
            return False

    def create_project(self, project):
        """
        Create a new project in Ringling
        :param project: The project to send to Ringling
        :return: The ID for the newly created project
        """
        obj = project.__dict__
        try:
            response = requests.post(self.project_url,
                                     json=obj, timeout=5)
            if handle_create(response):
                return response.json()['project_id']
        except RequestsConnectionError:
            connection_error()
        return None

    def create_param_set(self, param_set):
        """
        Create a new parameter set in Ringling
        :param param_set: The parameter set to send to Ringling
        :return: The ID for the newly created parameter set
        """
        obj = {"project_id": param_set.project_id,
               "training_parameters": param_set.training_parameters,
               "is_active": param_set.is_active,
               "metadata": param_set.metadata}

        try:
            response = requests.post(self.param_url,
                                     json=obj, timeout=5)
            if handle_create(response):
                return response.json()['parameter_set_id']
            return None
        except RequestsConnectionError:
            connection_error()
        return None

    def create_trained_model(self, trained_model):
        """
        Create a new trained model in Ringling
        :param trained_model: The trained model to send to Ringling
        :return: The ID for the newly created trained model
        """
        obj = trained_model.__dict__

        try:
            response = requests.post(self.trained_model_url,
                                     json=obj, timeout=5)
            if handle_create(response):
                return response.json()['model_id']
        except RequestsConnectionError:
            connection_error()
        return None

    def create_model_test(self, model_test):
        """
        Create a new model test in Ringling
        :param model_test: The model test to send to Ringling
        :return: The ID for the newly created model test
        """
        obj = model_test.__dict__
        try:
            response = requests.post(self.model_test_url,
                                     json=obj, timeout=5)
            if handle_create(response):
                return response.json()['test_id']
        except RequestsConnectionError:
            connection_error()
        return None

    def get_project(self, cur_id):
        """
        Get a project from Ringling given an id
        :param cur_id: the id to retrieve
        :return: The Project object
        """
        url = self.project_url + "/" + str(cur_id)
        try:
            response = requests.get(url, timeout=5)
            return json_to_project(handle_get(response, "Project", cur_id))
        except RequestsConnectionError:
            connection_error()
        return None

    def get_param_set(self, cur_id):
        """
        Get a parameter set from Ringling given an id
        :param cur_id: the id to retrieve
        :return: the ParameterSet object
        """
        url = self.param_url + "/" + str(cur_id)
        try:
            response = requests.get(url, timeout=5)
            return json_to_param_set(handle_get(response, "Parameter Set", cur_id))
        except RequestsConnectionError:
            connection_error()
        return None

    def get_trained_model(self, cur_id):
        """
        Get a trained model from Ringling given an id
        :param cur_id: the id to retrieve
        :return: TrainedModel object
        """
        url = self.trained_model_url + "/" + str(cur_id)
        try:
            response = requests.get(url, timeout=5)
            return json_to_trained_model(handle_get(response, "Trained Model", cur_id))
        except RequestsConnectionError:
            connection_error()
        return None

    def get_model_test(self, cur_id):
        """
        Get a model test from Ringling given an ID
        :param cur_id: the id to retrieve
        :return: ModelTest object
        """
        url = self.model_test_url + "/" + str(cur_id)
        try:
            response = requests.get(url, timeout=5)
            return json_to_model_test(handle_get(response, "Model Test", cur_id))
        except RequestsConnectionError:
            connection_error()
        return None

    def list_projects(self):
        """
        List all the projects in Ringling
        :return: A dictionary of id:Project for all projects
        """
        return obj_list(self.project_url, json_to_project)

    def list_param_sets(self):
        """
        List all the parameter sets in Ringling
        :return: A dictionary of id:ParameterSet for all parameter sets
        """
        return obj_list(self.param_url, json_to_param_set)

    def list_trained_models(self):
        """
        List all the trained models in Ringling
        :return: A dictionary of id:TrainedModel for all trained models
        """
        return obj_list(self.trained_model_url, json_to_trained_model)

    def list_model_tests(self):
        """
        List all the model tests in Ringling
        :return: A dictionary of id:ModelTest for all model tests
        """
        return obj_list(self.model_test_url, json_to_model_test)
