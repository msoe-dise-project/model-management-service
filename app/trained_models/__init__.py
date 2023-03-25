from flask import Blueprint

import datetime as dt

from flask import request
from flask.json import jsonify

import psycopg2
from psycopg2.extras import Json

from app.database import get_database_uri
from app.schemas import TrainedModelPatchSchema
from app.schemas import TrainedModelSchema
from app.schemas import ValidationError

blueprint = Blueprint("trained_models", __name__)

@blueprint.route('/v1/trained_models', methods=["POST"])
def create_trained_model():
    try:
        trained_model = TrainedModelSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            query = "INSERT INTO trained_models (project_id, parameter_set_id, training_data_from, training_data_until, model_object, train_timestamp, deployment_stage) " + \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s) " + \
                    "RETURNING model_id"

            cur.execute(query,
                        (trained_model.project_id,
                         trained_model.parameter_set_id,
                         trained_model.training_data_from,
                         trained_model.training_data_until,
                         trained_model.model_object,
                         trained_model.train_timestamp,
                         trained_model.deployment_stage))

            model_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({"model_id" : model_id}), 201
    
@blueprint.route('/v1/trained_models', methods=["GET"])
def list_models():
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT model_id, project_id, parameter_set_id, training_data_from, training_data_until, train_timestamp, deployment_stage, model_object FROM trained_models')

            models = []
            for model_id, project_id, parameter_set_id, data_start, data_end, train_timestamp, deployment_stage, model_object in cur:
                models.append(
                    {
                        "model_id" : model_id,
                        "project_id" : project_id,
                        "parameter_set_id" : parameter_set_id,
                        "training_data_from" : data_start.isoformat(),
                        "training_data_until" : data_end.isoformat(),
                        "train_timestamp" : train_timestamp.isoformat(),
                        "deployment_stage" : deployment_stage,
                        "model_object" : model_object
                    })
    
    conn.close()

    return jsonify({ "trained_models" : models })
    
@blueprint.route('/v1/trained_models/<int:model_id>', methods=["GET"])
def get_model_by_id(model_id):
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            query = "SELECT model_id, project_id, parameter_set_id, training_data_from, training_data_until, model_object, train_timestamp, deployment_stage " + \
                    "FROM trained_models WHERE model_id = %s"
            cur.execute(query, (model_id,))

            model_id, project_id, parameter_set_id, data_start, data_end, model_object, train_timestamp, deployment_stage = cur.fetchone()
            model = {
                        "model_id" : model_id,
                        "project_id" : project_id,
                        "parameter_set_id" : parameter_set_id,
                        "training_data_from" : data_start.isoformat(),
                        "training_data_until" : data_end.isoformat(),
                        "model_object" : model_object,
                        "train_timestamp" : train_timestamp.isoformat(),
                        "deployment_stage" : deployment_stage
                    }
    
    conn.close()

    return jsonify(model)

@blueprint.route('/v1/trained_models/<int:model_id>', methods=["PATCH"])
def update_trained_model(model_id):
    try:
        patch = TrainedModelPatchSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            query = "UPDATE trained_models SET deployment_stage = %s " + \
                    "WHERE model_id = %s " + \
                    "RETURNING model_id"

            cur.execute(query,
                        (patch.deployment_stage,
                         model_id))

            model_id = cur.fetchone()[0]

    conn.commit()
    
    conn.close()

    return jsonify({ "model_id" : model_id, "is_active" : patch.deployment_stage })