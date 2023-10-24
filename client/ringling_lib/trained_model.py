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

"""
Module for Trained Model objects
"""
# pylint: disable=R0801

from .utils import validate_types
from .utils import validate_iso
class TrainedModel:
    """
    Object for trained models fields
    """
    def __init__(self, project_id, parameter_set_id, training_data_from,
                 training_data_until, model_object,
                 train_timestamp, deployment_stage, backtest_timestamp,
                 backtest_metrics, passed_backtesting, metadata=None):
        """
        Initialize a new trained model
        :param project_id: The project ID of the trained model
        :param parameter_set_id: The parameter set ID that the trained model is trained from
        :param training_data_from: The start date for training data
        :param training_data_until: The end date for training data
        :param model_object: The pickled, serialized trained model object
        :param train_timestamp: The timestamp that the model was trained
        :param deployment_stage: The deployment stage of the model
        :param backtest_timestamp: The timestamp for when the model was backtested
        :param backtest_metrics: The metrics for backtesting
        :param passed_backtesting: If the model passed backtesting or not
        :param metadata: Any additional data to store with the trained model
        """
        if metadata is None:
            metadata = {}

        params = [(project_id, int),
                  (parameter_set_id, int),
                  (training_data_from, str),
                  (training_data_until, str),
                  (model_object, str),
                  (train_timestamp, str),
                  (deployment_stage, str),
                  (backtest_timestamp, str),
                  (backtest_metrics, dict),
                  (passed_backtesting, bool),
                  (metadata, dict)]

        validate_types(params)

        timestamps = {
            'training_data_from': training_data_from,
            'training_data_until': training_data_until,
            'train_timestamp': train_timestamp,
            'backtest_timestamp': backtest_timestamp,
        }

        for key, value in timestamps.items():
            if not validate_iso(value):
                raise ValueError(f'{key} with value of {value} is not in ISO-8601 format')

        if deployment_stage not in ["testing", "production", "retired"]:
            raise ValueError(f'deployment_stage with value \"{deployment_stage}\" must be one of: '
                             f'["testing", "production", "retired"]')
        self.project_id = project_id
        self.parameter_set_id = parameter_set_id
        self.training_data_from = training_data_from
        self.training_data_until = training_data_until
        self.model_object = model_object
        self.train_timestamp = train_timestamp
        self.deployment_stage = deployment_stage
        self.backtest_timestamp = backtest_timestamp
        self.backtest_metrics = backtest_metrics
        self.passed_backtesting = passed_backtesting
        self.metadata = metadata
