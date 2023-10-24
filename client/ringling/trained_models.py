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
from ringling_lib.trained_model import TrainedModel
from ringling_lib.ringling_db import RinglingDBSession
from .response_handling import handle_create
from .response_handling import handle_get
from .response_handling import handle_modify
from .response_handling import perform_list
from .response_handling import connection_error



def get_url(base_url):
    """
    Get the URL for interacting with trained models
    :return: The trained model URL
    """
    return base_url + "/v1/trained_models"


def create_trained_model(session, obj):
    """
    Create a trained model on the Ringling service
    :param session: An instance of a Ringling DB session
    :param obj: The model object
    :return: None
    """
    cur_id = session.create_trained_model(obj)
    print(f"Trained Model created with ID {cur_id}")

def get_trained_model(session, trained_model_id):
    """
    Get a trained model given an ID
    :param session: An instance of a Ringling DB session
    :param trained_model_id: The ID of the trained model
    :return: None
    """
    pprint.pprint(session.get_trained_model_json(trained_model_id))


def modify_trained_model(base_url, model_id, status):
    """
    Modify the deployment status of a trained model
    :param session: An instance of a Ringling DB session
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


def list_trained_models(session):
    """
    List all the trained models in the Ringling Service
    :param session: An instance of a Ringling DB session
    :return: None
    """
    pprint.pprint(session.list_trained_models_json())
