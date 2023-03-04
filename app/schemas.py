from marshmallow import Schema, fields, post_load

class Project:
    def __init__(self, project_name, project_start, project_id=None, project_end=None):
        self.project_name = project_name
        self.project_start = project_start
        self.project_id = project_id
        self.project_end = project_end

class ParameterSet:
    def __init__(self, project_id, training_parameters, minimum_software_version, parameter_set_id=None, active_from=None, active_until=None):
        self.project_id = project_id
        self.training_parameters = training_parameters
        self.minimum_software_version = minimum_software_version
        self.parameter_set_id = parameter_set_id
        self.active_from = active_from
        self.active_until = active_until

class TrainedModel:
    def __init__(self, project_id, parameter_set_id, training_data_from, training_data_until, model_object, train_timestamp, model_id=None, active_from=None, active_until=None):
        self.project_id = project_id
        self.parameter_set_id = parameter_set_id
        self.training_data_from = training_data_from
        self.training_data_until = training_data_until
        self.model_object = model_object
        self.train_timestamp = train_timestamp
        self.model_id = model_id
        self.active_from = active_from
        self.active_until = active_until
        
class ModelTest:
    def __init__(self, project_id, parameter_set_id, model_id, test_timestamp, test_metrics, passed_testing, test_id=None):
        self.test_id = test_id
        self.project_id = project_id
        self.parameter_set_id = parameter_set_id
        self.model_id = model_id
        self.test_timestamp = test_timestamp
        self.test_metrics = test_metrics
        self.passed_testing = passed_testing
        
class ActiveInterval:
    def __init__(self, active_from=None, active_until=None):
        self.active_from = active_from
        self.active_until = active_until

class ProjectSchema(Schema):
    project_id = fields.Integer()
    project_name = fields.String(required=True)
    project_start = fields.DateTime(required=True)
    project_end = fields.DateTime()
    
    @post_load
    def make_project(self, data, **kwargs):
        return Project(**data)
    
class ParameterSetSchema(Schema):
    parameter_set_id = fields.Integer()
    project_id = fields.Integer(required=True)
    # not sure how to indicate JSON-compatible hierarchy of Python collections 
    training_parameters = fields.Raw(required=True)
    minimum_software_version = fields.Integer(required=True)
    active_from = fields.DateTime()
    active_until = fields.DateTime()
    
    @post_load
    def make_parameter_set(self, data, **kwargs):
        return ParameterSet(**data)
    
class TrainedModelSchema(Schema):
    model_id = fields.Integer()
    project_id = fields.Integer(required=True)
    parameter_set_id = fields.Integer(required=True)
    training_data_from = fields.DateTime(required=True)
    training_data_until = fields.DateTime(required=True)
    model_object = fields.Raw(required=True)
    train_timestamp = fields.DateTime(required=True)
    active_from = fields.DateTime()
    active_until = fields.DateTime()
    
    @post_load
    def make_trained_model(self, data, **kwargs):
        return TrainedModel(**data)
        
class ModelTestSchema(Schema):
    test_id = fields.Integer()
    model_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    parameter_set_id = fields.Integer(required=True)
    test_timestamp = fields.DateTime(required=True)
    test_metrics = fields.Raw(required=True)
    passed_testing = fields.Boolean(required=True)
    
    @post_load
    def make_test_results(self, data, **kwargs):
        return ModelTest(**data)
        
class ActiveIntervalSchema(Schema):
    active_from = fields.DateTime()
    active_until = fields.DateTime()
    
    @post_load
    def make_active_interval(self, data, **kwargs):
        return ActiveInterval(**data)