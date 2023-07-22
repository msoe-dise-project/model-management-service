from flask import Blueprint

import datetime as dt

from flask import request
from flask.json import jsonify

import psycopg2
from psycopg2.extras import Json

from app.database import get_database_uri
from app.schemas import ModelTest
from app.schemas import ModelTestSchema
from app.schemas import ValidationError

blueprint = Blueprint("model_tests", __name__)

@blueprint.route('/v1/model_tests', methods=["POST"])
def create_trained_model():
    try:
        model_test = ModelTestSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            query = "INSERT INTO model_tests (project_id, parameter_set_id, model_id, test_timestamp, test_metrics, passed_testing) " + \
                    "VALUES (%s, %s, %s, %s, %s, %s) " + \
                    "RETURNING model_id"

            cur.execute(query,
                        (model_test.project_id,
                         model_test.parameter_set_id,
                         model_test.model_id,
                         model_test.test_timestamp,
                         Json(model_test.test_metrics),
                         model_test.passed_testing))

            test_id = cur.fetchone()[0]

        conn.commit()

    return jsonify({"test_id" : test_id}), 201
    
@blueprint.route('/v1/model_tests', methods=["GET"])
def list_models():
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT test_id, project_id, parameter_set_id, model_id, test_timestamp, test_metrics, passed_testing FROM model_tests')

            tests = [
                ModelTest(project_id, parameter_set_id, model_id, test_timestamp, test_metrics, passed_testing, test_id) \
                for test_id, project_id, parameter_set_id, model_id, test_timestamp, test_metrics, passed_testing in cur
            ]

    conn.close()

    return jsonify({ "model_tests" : tests })
    
@blueprint.route('/v1/model_tests/<int:test_id>', methods=["GET"])
def get_model_by_id(test_id):
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            query = "SELECT test_id, project_id, parameter_set_id, model_id, test_timestamp, test_metrics, passed_testing " + \
                    "FROM model_tests WHERE test_id = %s"
            cur.execute(query, (test_id,))
            result = cur.fetchone()
            if result is None:
                return jsonify({"error": f"ID {test_id} not found"}), 404
            else:
                test_id, project_id, parameter_set_id, model_id, test_timestamp, test_metrics, passed_testing = result
                test = ModelTest(project_id, parameter_set_id, model_id, test_timestamp, test_metrics, passed_testing, test_id)
    
    conn.close()

    return jsonify(test)
