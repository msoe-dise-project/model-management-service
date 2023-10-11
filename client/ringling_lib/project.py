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
