"""
Module for project objects
"""
class Project:
    """
    Object for the project class
    """
    def __init__(self, project_name, metadata=None):
        """
        Initialize the project
        :param project_name: The name of the project
        :param metadata: Any additional data to store with the project
        """
        if metadata is None:
            metadata = {}
        self.project_name = project_name
        self.metadata = metadata
