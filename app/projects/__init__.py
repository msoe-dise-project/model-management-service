from flask import Blueprint

import datetime as dt

from flask import request
from flask.json import jsonify

from flask_expects_json import expects_json

import psycopg2
from psycopg2.extras import Json

from app.database import get_database_uri

blueprint = Blueprint("projects", __name__)

project_create_schema = {
  "type": "object",
  "properties": {
    "project_name": { "type": "string" },
    "project_start": { "type": "string" },
    "project_end" : { "type" : "string" }
  },
  "required": ["project_name", "project_start"]
}

@blueprint.route('/v1/projects', methods=["POST"])
@expects_json(project_create_schema)
def create_project():
    record = request.get_json()

    project_name = record["project_name"]
    project_start = dt.datetime.fromisoformat(record["project_start"])

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO projects (project_name, project_start) VALUES (%s, %s) RETURNING project_id',
                        (project_name,
                         project_start))

            project_id = cur.fetchone()[0]

            conn.commit()

    return jsonify({"project_id" : project_id})
    
@blueprint.route('/v1/projects', methods=["GET"])
def list_projects():
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT project_id, project_name, project_start, project_end FROM projects")
            
            projects = []
            for _id, _name, _start, _end in cur:
                project = {
                    "project_id" : _id,
                    "project_name" : _name,
                    "project_start" : None if _start is None else _start.isoformat(),
                    "project_end" : None if _end is None else _end.isoformat()
                }
                
                projects.append(project)

            conn.commit()

    return jsonify({"projects" : projects})
    
@blueprint.route('/v1/projects/<int:project_id>', methods=["GET"])
def get_project(project_id):
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT project_id, project_name, project_start, project_end FROM projects "
                        "WHERE project_id = %s",
                        (project_id,))
            
            _id, _name, _start, _end = cur.fetchone()
            
            project = {
                "project_id" : _id,
                "project_name" : _name,
                "project_start" : None if _start is None else _start.isoformat(),
                "project_end" : None if _end is None else end.isoformat()
            }

            conn.commit()

    return jsonify(project)

project_end_update_schema = {
  "type": "object",
  "properties": {
    "project_end" : { "type" : "string" }
  },
  "required": ["project_end"]
}


@blueprint.route('/v1/projects/<int:project_id>/project_end', methods=["PUT"])
@expects_json(project_end_update_schema)
def update_project_end(project_id):
    record = request.get_json()
    
    project_end = dt.datetime.fromisoformat(record["project_end"])
    
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE projects SET project_end = %s "
                        "WHERE project_id = %s",
                        (project_end, project_id))
            
            num_updated = cur.rowcount

            conn.commit()

    if num_updated == 0:
        return jsonify("Message could not find project with given id"), 404

    return jsonify({"num_projects_updated" : num_updated})