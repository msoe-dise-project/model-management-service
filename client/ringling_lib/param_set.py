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

Module for parameter set objects
"""

from .utils import validate_types
class ParameterSet:
    """
    Object for Parameter Set fields
    """
    def __init__(self, project_id, training_parameters, is_active, metadata=None):
        """
        Initialize the parameter set object
        :param project_id: The referenced project ID for the parameter set
        :param training_parameters: The parameters for the parameter set, maybe a pickled pipeline
        :param is_active: If the parameter set is active or not
        :param metadata: Any additional data to store with the parameter set
        """

        if metadata is None:
            metadata = {}

        params = [(project_id, int),
                  (is_active, bool),
                  (metadata, dict)]

        validate_types(params)

        if not isinstance(training_parameters, str) and not isinstance(training_parameters, dict):
            raise TypeError(f'{training_parameters} should be of type str or dict '
                            f'but is instead {type(training_parameters)}')

        self.project_id = project_id
        self.training_parameters = training_parameters
        self.is_active = is_active
        self.metadata = metadata
