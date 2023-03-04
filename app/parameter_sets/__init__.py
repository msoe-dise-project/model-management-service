from flask import Blueprint

import datetime as dt

from flask import request
from flask.json import jsonify

from flask_expects_json import expects_json

import psycopg2
from psycopg2.extras import Json

from app.database import get_database_uri

blueprint = Blueprint("parameter_sets", __name__)

parameter_set_create_schema = {
  "type": "object",
  "properties": {
    "project_id": { "type": "number" },
    "params": { "type": "object" },
    "active_from" : { "type" : "string" },
    "active_until" : { "type" : "string" }
  },
  "required": ["project_id", "params"]
}

@blueprint.route('/v1/parameter_sets', methods=["POST"])
@expects_json(parameter_set_create_schema)
def create_parameter_set():
    record = request.get_json()

    project_id = record["project_id"]
    active_from = None if "active_from" not in record or record["active_from"] is None else dt.datetime.fromisoformat(record["active_from"])
    active_until = None if "active_until" not in record or record["active_until"] is None else dt.datetime.fromisoformat(record["active_until"])
    params = record["params"]

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO parameter_sets (project_id, parameters, active_from, active_until) VALUES (%s, %s, %s, %s) RETURNING parameter_set_id',
                        (project_id,
                         Json(params),
                         active_from,
                         active_until))

            parameter_set_id = cur.fetchone()[0]

            conn.commit()

    return jsonify({"parameter_set_id" : parameter_set_id})
    
@blueprint.route('/v1/parameter_sets', methods=["GET"])
def list_parameter_sets():
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT parameter_set_id, project_id, parameters, active_from, active_until FROM parameter_sets')

            parameter_sets = []
            for parameter_set_id, project_id, params, active_from, active_until in cur:
                parameter_sets.append(
                    {
                        "parameter_set_id" : parameter_set_id,
                        "project_id" : project_id,
                        "params" : params,
                        "active_from" : None if active_from is None else active_from.isoformat(),
                        "active_until" : None if active_until is None else active_until.isoformat()
                    })

    return jsonify({ "parameter_sets" : parameter_sets })

@blueprint.route('/v1/parameter_sets/<int:parameter_set_id>', methods=["GET"])
def get_parameter_set(parameter_set_id):
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT parameter_set_id, project_id, parameters, active_from, active_until FROM parameter_sets WHERE parameter_set_id = %s',
                        (parameter_set_id,))

            params_id, project_id, params, active_from, active_until = cur.fetchone()

            obj = { "parameter_set_id" : params_id,
                    "project_id" : project_id,
                    "params" : params,
                    "active_from" : None if active_from is None else active_from.isoformat(),
                    "active_until" : None if active_until is None else active_until.isoformat() }

    return jsonify(obj)

parameter_set_update_schema = {
  "type": "object",
  "properties": {
    "active_from" : { "type" : "string" },
    "active_until" : { "type" : "string" }
  }
}

@blueprint.route('/v1/parameter_sets/<int:parameter_set_id>', methods=["PUT"])
@expects_json(parameter_set_update_schema)
def update_parameter_set_active_interval(parameter_set_id):
    record = request.get_json()

    active_from_present = "active_from" in record and record["active_from"] is not None
    active_until_present = "active_until" in record and record["active_until"] is not None
    
    active_from = None if "active_from" not in record or record["active_from"] is None else dt.datetime.fromisoformat(record["active_from"])
    active_until = None if "active_until" not in record or record["active_until"] is None else dt.datetime.fromisoformat(record["active_until"])

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            
            if active_from_present and active_until_present:
                cur.execute('UPDATE parameter_sets SET active_from = %s, active_until = %s WHERE parameter_set_id = %s RETURNING parameter_set_id, project_id, parameters, active_from, active_until',
                            (active_from,
                             active_until,
                             parameter_set_id))
            elif active_from_present:
                cur.execute('UPDATE parameter_sets SET active_from = %s WHERE parameter_set_id = %s RETURNING parameter_set_id, project_id, parameters, active_from, active_until',
                            (active_from,
                             parameter_set_id))
            elif active_until_present:
                cur.execute('UPDATE parameter_sets SET active_until = %s WHERE parameter_set_id = %s RETURNING parameter_set_id, project_id, parameters, active_from, active_until',
                            (active_until,
                             parameter_set_id))

            parameter_set_id, project_id, params, active_from, active_until = cur.fetchone()

            conn.commit()

    return jsonify({
        "parameter_set_id" : parameter_set_id,
        "project_id" : project_id, 
        "params" : params,
        "active_from" : None if active_from is None else active_from.isoformat(),
        "active_until" : None if active_until is None else active_until.isoformat()
    })
