from flask import Blueprint

import datetime as dt

from flask import request
from flask.json import jsonify

import psycopg2
from psycopg2.extras import Json

from app.database import get_database_uri
from app.schemas import ParameterSetSchema
from app.schemas import ActiveIntervalSchema

blueprint = Blueprint("parameter_sets", __name__)

@blueprint.route('/v1/parameter_sets', methods=["POST"])
def create_parameter_set():
    record = request.get_json()

    trained_model = ParameterSetSchema().load(record)

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO parameter_sets (project_id, training_parameters, minimum_software_version, active_from, active_until) VALUES (%s, %s, %s, %s, %s) RETURNING parameter_set_id',
                        (trained_model.project_id,
                         Json(trained_model.training_parameters),
                         trained_model.minimum_software_version,
                         trained_model.active_from,
                         trained_model.active_until))

            parameter_set_id = cur.fetchone()[0]

            conn.commit()

    return jsonify({"parameter_set_id" : parameter_set_id})
    
@blueprint.route('/v1/parameter_sets', methods=["GET"])
def list_parameter_sets():
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT parameter_set_id, project_id, training_parameters, minimum_software_version, active_from, active_until FROM parameter_sets')

            parameter_sets = []
            for parameter_set_id, project_id, params, min_version, active_from, active_until in cur:
                parameter_sets.append(
                    {
                        "parameter_set_id" : parameter_set_id,
                        "project_id" : project_id,
                        "training_parameters" : params,
                        "minimum_software_version" : min_version,
                        "active_from" : None if active_from is None else active_from.isoformat(),
                        "active_until" : None if active_until is None else active_until.isoformat()
                    })

    return jsonify({ "parameter_sets" : parameter_sets })

@blueprint.route('/v1/parameter_sets/<int:parameter_set_id>', methods=["GET"])
def get_parameter_set(parameter_set_id):
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT parameter_set_id, project_id, training_parameters, minimum_software_version, active_from, active_until FROM parameter_sets WHERE parameter_set_id = %s',
                        (parameter_set_id,))

            params_id, project_id, params, min_version, active_from, active_until = cur.fetchone()

            obj = { "parameter_set_id" : params_id,
                    "project_id" : project_id,
                    "training_parameters" : params,
                    "minimum_software_version" : min_version,
                    "active_from" : None if active_from is None else active_from.isoformat(),
                    "active_until" : None if active_until is None else active_until.isoformat() }

    return jsonify(obj)

@blueprint.route('/v1/parameter_sets/<int:parameter_set_id>', methods=["PUT"])
def update_parameter_set_active_interval(parameter_set_id):
    active_interval = ActiveIntervalSchema().load(request.get_json())
    
    if active_interval.active_until is not None and active_interval.active_from is None:
        return jsonify({ "error" : "If an end date is specified, a start date must also be specified"}), 400
        
    if active_interval.active_from >= active_interval.active_until:
        return jsonify({ "error" : "The start date must be strictly before the end date."}), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE parameter_sets SET active_from = %s, active_until = %s WHERE parameter_set_id = %s RETURNING parameter_set_id',
                        (active_interval.active_from,
                         active_interval.active_until,
                         parameter_set_id))

            parameter_set_id = cur.fetchone()[0]

            conn.commit()

    return jsonify({
        "parameter_set_id" : parameter_set_id,
        "active_from" : None if active_interval.active_from is None else active_interval.active_from.isoformat(),
        "active_until" : None if active_interval.active_until is None else active_interval.active_until.isoformat()
    })
