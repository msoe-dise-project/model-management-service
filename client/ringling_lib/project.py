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
Module for project objects
"""

from .utils import validate_types
class Project:
    """
    Object for the project class
    """
    def __init__(self, project_name: str, metadata: dict = None):
        """
        Initialize the project
        :param project_name: The name of the project
        :param metadata: Any additional data to store with the project
        """

        if metadata is None:
            metadata = {}

        params = [(project_name, str),
                  (metadata, dict)]

        validate_types(params)

        self.project_name = project_name
        self.metadata = metadata
