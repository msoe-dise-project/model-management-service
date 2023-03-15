from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema

# import this so it can be imported from this module
# by users of this module.  this avoids other modules
# directly depending on marshmallow
from marshmallow import ValidationError

class Project:
    def __init__(self, project_name, project_id=None):
        self.project_name = project_name
        self.project_id = project_id

class ParameterSet:
    def __init__(self, project_id, training_parameters, is_active, parameter_set_id=None):
        self.project_id = project_id
        self.training_parameters = training_parameters
        self.parameter_set_id = parameter_set_id
        self.is_active = is_active
        
class ParameterSetPatch:
    def __init__(self, is_active):
        self.is_active = is_active

class TrainedModel:
    def __init__(self, project_id, parameter_set_id, training_data_from, training_data_until, model_object, train_timestamp, deployment_stage, model_id=None):
        self.project_id = project_id
        self.parameter_set_id = parameter_set_id
        self.training_data_from = training_data_from
        self.training_data_until = training_data_until
        self.model_object = model_object
        self.train_timestamp = train_timestamp
        self.deployment_stage = deployment_stage
        self.model_id = model_id
        
class TrainedModelPatch:
    def __init__(self, deployment_stage):
        self.deployment_stage = deployment_stage
        
class ModelTest:
    def __init__(self, project_id, parameter_set_id, model_id, test_timestamp, test_metrics, passed_testing, test_id=None):
        self.test_id = test_id
        self.project_id = project_id
        self.parameter_set_id = parameter_set_id
        self.model_id = model_id
        self.test_timestamp = test_timestamp
        self.test_metrics = test_metrics
        self.passed_testing = passed_testing

class ProjectSchema(Schema):
    project_id = fields.Integer()
    project_name = fields.String(required=True)
    
    @post_load
    def make_project(self, data, **kwargs):
        return Project(**data)
    
class ParameterSetSchema(Schema):
    project_id = fields.Integer(required=True)
    parameter_set_id = fields.Integer()
    training_parameters = fields.String(required=True)
    is_active = fields.Boolean(required=True)
    
    @post_load
    def make_parameter_set(self, data, **kwargs):
        return ParameterSet(**data)
        
class ParameterSetPatchSchema(Schema):
    is_active = fields.Boolean(required=True)
    
    @post_load
    def make_parameter_set_patch(self, data, **kwargs):
        return ParameterSetPatch(**data)
    
class TrainedModelSchema(Schema):
    project_id = fields.Integer(required=True)
    parameter_set_id = fields.Integer(required=True)
    model_id = fields.Integer()
    training_data_from = fields.DateTime(required=True)
    training_data_until = fields.DateTime(required=True)
    model_object = fields.String(required=True)
    train_timestamp = fields.DateTime(required=True)
    deployment_stage = fields.String(required=True)
    
    @post_load
    def make_trained_model(self, data, **kwargs):
        return TrainedModel(**data)
        
class TrainedModelPatchSchema(Schema):
    deployment_stage = fields.String(required=True)
    
    @post_load
    def make_trained_model_patch(self, data, **kwargs):
        return TrainedModelPatch(**data)
        
class ModelTestSchema(Schema):
    model_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    parameter_set_id = fields.Integer(required=True)
    test_id = fields.Integer()
    test_timestamp = fields.DateTime(required=True)
    test_metrics = fields.Raw(required=True)
    passed_testing = fields.Boolean(required=True)
    
    @post_load
    def make_test_results(self, data, **kwargs):
        return ModelTest(**data)