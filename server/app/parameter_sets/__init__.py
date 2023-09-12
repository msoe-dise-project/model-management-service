"""
The parameter sets module
Used to perform actions with parameter sets such as Scikit-learn pipelines
"""


import datetime as dt

from flask import Blueprint

from flask import request
from flask.json import jsonify

import psycopg2
from psycopg2.extras import Json

from app.database import get_database_uri
from app.schemas import ParameterSet
from app.schemas import ParameterSetPatch
from app.schemas import ParameterSetPatchSchema
from app.schemas import ParameterSetSchema
from app.schemas import ValidationError

blueprint = Blueprint("parameter_sets", __name__)

@blueprint.route('/v1/parameter_sets', methods=["POST"])
def create_parameter_set():
    """
    Create a new parameter set in Ringling
    :return: The ID of the newly created parameter set, status code
    """
    try:
        record = request.get_json()
        parameter_set = ParameterSetSchema().load(record)
    except ValidationError as err:
        return jsonify(err.messages), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO parameter_sets (project_id, training_parameters, is_active)'
                        ' VALUES (%s, %s, %s) RETURNING parameter_set_id',
                        (parameter_set.project_id,
                         Json(parameter_set.training_parameters),
                         parameter_set.is_active))

            parameter_set_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({"parameter_set_id" : parameter_set_id}), 201

@blueprint.route('/v1/parameter_sets', methods=["GET"])
def list_parameter_sets():
    """
    Retrieve all parameter sets from Ringling
    :return: The parameter sets as a JSON object
    """
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT parameter_set_id, project_id, '
                        'training_parameters, is_active FROM parameter_sets')

            parameter_sets = [
                ParameterSet(project_id, params, is_active, parameter_set_id) \
                for parameter_set_id, project_id, params, is_active in cur
            ]

    conn.close()

    return jsonify({ "parameter_sets" : parameter_sets })

@blueprint.route('/v1/parameter_sets/<int:parameter_set_id>', methods=["GET"])
def get_parameter_set(parameter_set_id):
    """
    Retrieve a parameter set from Ringling by ID
    :param parameter_set_id: The parameter set ID to retrieve
    :return: the parameter set as a JSON object
    """
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT parameter_set_id, project_id, training_parameters,'
                        ' is_active FROM parameter_sets WHERE parameter_set_id = %s',
                        (parameter_set_id,))

            result = cur.fetchone()
            if result is None:
                return jsonify({"error": f"ID {parameter_set_id} not found"}), 404
            params_id, project_id, params, is_active = result
            obj = ParameterSet(project_id, params, is_active, params_id)

    conn.close()

    return jsonify(obj)

@blueprint.route('/v1/parameter_sets/<int:parameter_set_id>', methods=["PATCH"])
def update_parameter_set_status(parameter_set_id):
    """
    Update the activity status of a parameter set from Ringling by ID
    :param parameter_set_id: The parameter set ID to update
    :return: the patched parameter set
    """
    try:
        patch = ParameterSetPatchSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE parameter_sets SET is_active = %s '
                        'WHERE parameter_set_id = %s RETURNING parameter_set_id',
                        (patch.is_active,
                         parameter_set_id))
            result = cur.fetchone()
            if result is None:
                return jsonify({"error": f"ID {parameter_set_id} not found"}), 404
            parameter_set_id = result[0]
            patch.parameter_set_id = parameter_set_id

    conn.commit()
    conn.close()

    return jsonify(patch)
