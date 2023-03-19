from flask import Blueprint

import datetime as dt

from flask import request
from flask.json import jsonify

import psycopg2
from psycopg2.extras import Json

from app.database import get_database_uri
from app.schemas import ParameterSetPatchSchema
from app.schemas import ParameterSetSchema
from app.schemas import ValidationError

blueprint = Blueprint("parameter_sets", __name__)

@blueprint.route('/v1/parameter_sets', methods=["POST"])
def create_parameter_set():
    try:
        record = request.get_json()
        trained_model = ParameterSetSchema().load(record)
    except ValidationError as err:
        return jsonify(err.messages), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO parameter_sets (project_id, training_parameters, is_active) VALUES (%s, %s, %s) RETURNING parameter_set_id',
                        (trained_model.project_id,
                         Json(trained_model.training_parameters),
                         trained_model.is_active))

            parameter_set_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({"parameter_set_id" : parameter_set_id}), 201
    
@blueprint.route('/v1/parameter_sets', methods=["GET"])
def list_parameter_sets():
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT parameter_set_id, project_id, training_parameters, is_active FROM parameter_sets')

            parameter_sets = []
            for parameter_set_id, project_id, params, is_active in cur:
                parameter_sets.append(
                    {
                        "parameter_set_id" : parameter_set_id,
                        "project_id" : project_id,
                        "training_parameters" : params,
                        "is_active" : is_active
                    })
    
    conn.close()

    return jsonify({ "parameter_sets" : parameter_sets })

@blueprint.route('/v1/parameter_sets/<int:parameter_set_id>', methods=["GET"])
def get_parameter_set(parameter_set_id):
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT parameter_set_id, project_id, training_parameters, is_active FROM parameter_sets WHERE parameter_set_id = %s',
                        (parameter_set_id,))

            params_id, project_id, params, is_active = cur.fetchone()

            obj = { "parameter_set_id" : params_id,
                    "project_id" : project_id,
                    "training_parameters" : params,
                    "is_active" : is_active
            }
    
    conn.close()

    return jsonify(obj)

@blueprint.route('/v1/parameter_sets/<int:parameter_set_id>', methods=["PATCH"])
def update_parameter_set_status(parameter_set_id):
    try:
        patch = ParameterSetPatchSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE parameter_sets SET is_active = %s WHERE parameter_set_id = %s RETURNING parameter_set_id',
                        (patch.is_active,
                         parameter_set_id))

            parameter_set_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({
        "parameter_set_id" : parameter_set_id,
        "is_active" : patch.is_active
    })
