"""
The schemas module
Contains the frameworks for all object types stored in Ringling
"""

from flask.json.provider import DefaultJSONProvider

from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema

# import this so it can be imported from this module
# by users of this module.  this avoids other modules
# directly depending on marshmallow
from marshmallow import ValidationError

class Project:
    """
    Object for the project class fields
    """
    def __init__(self, project_name, project_id=None):
        """
        Initialize the project
        :param project_name: The name of the project
        :param project_id: The ID of the project
        """
        self.project_name = project_name
        self.project_id = project_id

class ParameterSet:
    """
    Object for Parameter Set fields
    """
    def __init__(self, project_id, training_parameters, is_active, parameter_set_id=None):
        """
        Initialize the parameter set object
        :param project_id: The referenced project ID for the parameter set
        :param training_parameters: The parameters for the parameter set, generally a pickled pipeline
        :param is_active: If the parameter set is active or not
        :param parameter_set_id: The ID for the parameter set
        """
        self.project_id = project_id
        self.training_parameters = training_parameters
        self.parameter_set_id = parameter_set_id
        self.is_active = is_active

class ParameterSetPatch:
    """
    Object for activity status updates for parameter set fields
    """
    def __init__(self, is_active, parameter_set_id=None):
        """
        Initialize a parameter set update
        :param is_active: If the updated parameter set is active
        :param parameter_set_id: The parameter set ID to update
        """
        self.is_active = is_active
        self.parameter_set_id = parameter_set_id

class TrainedModel:
    """
    Object for trained models fields
    """
    def __init__(self, project_id, parameter_set_id, training_data_from,
                 training_data_until, model_object,
                 train_timestamp, deployment_stage, backtest_timestamp,
                 backtest_metrics, passed_backtesting, model_id=None):
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
        :param model_id: The ID for the model
        """
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
        self.model_id = model_id

class TrainedModelPatch:
    """
    Object for deployment stage updates for trained models
    """
    def __init__(self, deployment_stage, model_id=None):
        """
        Initialize a trained model update
        :param deployment_stage: The updated deployment stage of the trained model
        :param model_id: The ID of the trained model to update
        """
        self.deployment_stage = deployment_stage
        self.model_id = model_id

class ModelTest:
    """
    Object for model test fields
    """
    def __init__(self, project_id, parameter_set_id, model_id, test_timestamp,
                 test_metrics, passed_testing, test_id=None):
        """
        Initialize a new model test
        :param project_id: The project ID referenced by the model test
        :param parameter_set_id: The parameter set ID referenced by the model test
        :param model_id: The model ID that is being tested
        :param test_timestamp: The timestamp of the test
        :param test_metrics: Performance metrics for testing
        :param passed_testing: If the model passed testing or not
        :param test_id: The ID for the test
        """
        self.test_id = test_id
        self.project_id = project_id
        self.parameter_set_id = parameter_set_id
        self.model_id = model_id
        self.test_timestamp = test_timestamp
        self.test_metrics = test_metrics
        self.passed_testing = passed_testing

class ProjectSchema(Schema):
    """
    Schema for projects
    """
    project_id = fields.Integer()
    project_name = fields.String(required=True)

    @post_load
    def make_project(self, data, **kwargs):
        """
        Create a project
        :param data: Data for the project
        :param kwargs: Additional keyword arguments
        :return: A ready project
        """
        return Project(**data)

class ParameterSetSchema(Schema):
    """
    Schema for parameter sets
    """
    project_id = fields.Integer(required=True)
    parameter_set_id = fields.Integer()
    training_parameters = fields.Raw(required=True)
    is_active = fields.Boolean(required=True)

    @post_load
    def make_parameter_set(self, data, **kwargs):
        """
        Create a parameter set
        :param data: Data for the parameter set
        :param kwargs: Additional keyword arguments
        :return: A ready parameter set
        """
        return ParameterSet(**data)

class ParameterSetPatchSchema(Schema):
    """
    Schema for parameter set patches
    """
    is_active = fields.Boolean(required=True)
    parameter_set_id = fields.Integer()

    @post_load
    def make_parameter_set_patch(self, data, **kwargs):
        """
        Create a parameter set patch
        :param data: Data for the parameter set patch
        :param kwargs: Additional keyword arguments
        :return: A ready patch for a parameter set
        """
        return ParameterSetPatch(**data)

class TrainedModelSchema(Schema):
    """
    Schema for trained models
    """
    project_id = fields.Integer(required=True)
    parameter_set_id = fields.Integer(required=True)
    model_id = fields.Integer()
    training_data_from = fields.DateTime(required=True)
    training_data_until = fields.DateTime(required=True)
    model_object = fields.String(required=True)
    train_timestamp = fields.DateTime(required=True)
    deployment_stage = fields.String(required=True)
    backtest_timestamp = fields.DateTime(required=True)
    backtest_metrics = fields.Raw(required=True)
    passed_backtesting = fields.Boolean(required=True)

    @post_load
    def make_trained_model(self, data, **kwargs):
        """
        Create a trained model
        :param data: Data for the trained model
        :param kwargs: Additional keyword arguments
        :return: A ready trained model
        """
        return TrainedModel(**data)

class TrainedModelPatchSchema(Schema):
    """
    Schema for trained model patches
    """
    deployment_stage = fields.String(required=True)
    model_id = fields.Integer()

    @post_load
    def make_trained_model_patch(self, data, **kwargs):
        """
        Create a trained model patch
        :param data: Data for the trained model patch
        :param kwargs: Additional keyword arguments
        :return: A ready trained model patch
        """
        return TrainedModelPatch(**data)


class ModelTestSchema(Schema):
    """
    Schema for model tests
    """
    model_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    parameter_set_id = fields.Integer(required=True)
    test_id = fields.Integer()
    test_timestamp = fields.DateTime(required=True)
    test_metrics = fields.Raw(required=True)
    passed_testing = fields.Boolean(required=True)

    @post_load
    def make_test_results(self, data, **kwargs):
        """
        Create a model test
        :param data: Data for the model test
        :param kwargs: Additional keyword arguments
        :return: A ready model test
        """
        return ModelTest(**data)

class CustomJSONProvider(DefaultJSONProvider):
    """
    Convert schemas to json objects
    """
    @staticmethod
    def default(obj):
        """
        Method to convert schema objects to json
        :param obj: The object to dump
        :return: JSON with all the values according to the schema
        """
        if isinstance(obj, Project):
            return ProjectSchema().dump(obj)
        elif isinstance(obj, ParameterSetPatch):
            return ParameterSetPatchSchema().dump(obj)
        elif isinstance(obj, ParameterSet):
            return ParameterSetSchema().dump(obj)
        elif isinstance(obj, TrainedModel):
            return TrainedModelSchema().dump(obj)
        elif isinstance(obj, TrainedModelPatch):
            return TrainedModelPatchSchema().dump(obj)
        elif isinstance(obj, ModelTest):
            return ModelTestSchema().dump(obj)

        return DefaultJSONProvider.default(obj)
