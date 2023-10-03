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
