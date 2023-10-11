"""
Module for model test objects
"""

from .utils import validate_types
from .utils import validate_iso

class ModelTest:
    """
    Object for model test fields
    """
    def __init__(self, project_id, parameter_set_id, model_id, test_timestamp,
                 test_metrics, passed_testing, metadata=None):
        """
        Initialize a new model test
        :param project_id: The project ID referenced by the model test
        :param parameter_set_id: The parameter set ID referenced by the model test
        :param model_id: The model ID that is being tested
        :param test_timestamp: The timestamp of the test
        :param test_metrics: Performance metrics for testing
        :param passed_testing: If the model passed testing or not
        :param metadata: Any additional data to store with the trained model
        """
        if metadata is None:
            metadata = {}

        params = [(project_id, int),
                  (parameter_set_id, int),
                  (model_id, int),
                  (test_timestamp, str),
                  (test_metrics, dict),
                  (passed_testing, bool),
                  (metadata, dict)]

        validate_types(params)

        if not validate_iso(test_timestamp):
            raise ValueError(f'test_timestamp with value of '
                             f'{test_timestamp} is not in ISO-8601 format')

        self.project_id = project_id
        self.parameter_set_id = parameter_set_id
        self.model_id = model_id
        self.test_timestamp = test_timestamp
        self.test_metrics = test_metrics
        self.passed_testing = passed_testing
        self.metadata = metadata
