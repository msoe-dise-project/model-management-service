"""
Module for model test objects
"""
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
        self.project_id = project_id
        self.parameter_set_id = parameter_set_id
        self.model_id = model_id
        self.test_timestamp = test_timestamp
        self.test_metrics = test_metrics
        self.passed_testing = passed_testing
        self.metadata = metadata
