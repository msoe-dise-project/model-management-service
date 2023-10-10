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
from .response_handling import handle_modify
from .response_handling import perform_list
from .response_handling import connection_error
from ringling_lib.trained_model import TrainedModel
from ringling_lib.ringling_db import RinglingDBSession


def get_url(base_url):
    """
    Get the URL for interacting with trained models
    :return: The trained model URL
    """
    return base_url + "/v1/trained_models"


def create_trained_model(base_url, obj):
    """
    Create a trained model on the Ringling service
    :param base_url: The URL of the Ringling Service
    :param obj: The model object payload
    :return: None
    """
    try:
        response = requests.post(get_url(base_url),
                                 json=obj, timeout=5)
        if handle_create(response):
            print(f"Trained model created with ID {response.json()['model_id']}")
    except RequestsConnectionError:
        connection_error()


def get_trained_model(base_url, trained_model_id):
    """
    Get a trained model given an ID
    :param base_url: The URL of the Ringling Service
    :param trained_model_id: The ID of the trained model
    :return: None
    """
    url = get_url(base_url) + "/" + str(trained_model_id)
    try:
        response = requests.get(url, timeout=5)
        handle_get(response, "Trained Model", trained_model_id)
    except RequestsConnectionError:
        connection_error()


def modify_trained_model(base_url, model_id, status):
    """
    Modify the deployment status of a trained model
    :param base_url: The URL of the Ringling Service
    :param model_id: The ID of the trained model
    :param status: The current deployment status of the model
    :return: None
    """
    url = get_url(base_url) + "/" + str(model_id)
    update = {"deployment_stage": status}
    try:
        response = requests.patch(url, json=update, timeout=5)
        if handle_modify(response, "Trained Model", model_id):
            print("Trained Model", model_id, "deployment status changed to", status)
    except RequestsConnectionError:
        connection_error()


def list_trained_models(base_url):
    """
    List all the trained models in the Ringling Service
    :param base_url: The URL of the Ringling Service
    :return: None
    """
    perform_list(get_url(base_url))
