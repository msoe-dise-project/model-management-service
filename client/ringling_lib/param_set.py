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
        self.project_id = project_id
        self.training_parameters = training_parameters
        self.is_active = is_active
        self.metadata = metadata
