"""
The model tests module
Used to perform actions with regard to data drift testing for models
"""
import datetime as dt

from flask import Blueprint

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
    """
    Create a new model test in Ringling
    :return: The ID of the newly created model test, status code
    """
    try:
        model_test = ModelTestSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            query = "INSERT INTO model_tests (project_id, parameter_set_id, " \
                    "model_id, test_timestamp, test_metrics, passed_testing) " + \
                    "VALUES (%s, %s, %s, %s, %s, %s) " + \
                    "RETURNING test_id"

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
    """
    Retrieve all model tests from Ringling
    :return: The model test as a JSON object
    """
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT test_id, project_id, parameter_set_id, '
                        'model_id, test_timestamp, test_metrics, passed_testing FROM model_tests')

            tests = [
                ModelTest(project_id, parameter_set_id, model_id,
                          test_timestamp, test_metrics, passed_testing, test_id) \
                for test_id, project_id, parameter_set_id, model_id,
                test_timestamp, test_metrics, passed_testing in cur
            ]

    conn.close()

    return jsonify({ "model_tests" : tests })

@blueprint.route('/v1/model_tests/<int:test_id>', methods=["GET"])
def get_model_by_id(test_id):
    """
    Retrieve a model from Ringling by ID
    :param test_id: The model test ID to retrieve
    :return: the model test as a JSON object
    """
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            query = "SELECT test_id, project_id, parameter_set_id, " \
                    "model_id, test_timestamp, test_metrics, passed_testing " + \
                    "FROM model_tests WHERE test_id = %s"
            cur.execute(query, (test_id,))
            result = cur.fetchone()
            if result is None:
                return jsonify({"error": f"ID {test_id} not found"}), 404
            test_id, project_id, parameter_set_id, \
                model_id, test_timestamp, test_metrics, passed_testing = result
            test = ModelTest(project_id, parameter_set_id, model_id,
                             test_timestamp, test_metrics, passed_testing, test_id)

    conn.close()

    return jsonify(test)
