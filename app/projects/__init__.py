from flask import Blueprint

import datetime as dt

from flask import request
from flask.json import jsonify

import psycopg2
from psycopg2.extras import Json

from app.database import get_database_uri
from app.schemas import ProjectSchema

blueprint = Blueprint("projects", __name__)

@blueprint.route('/v1/projects', methods=["POST"])
def create_project():
    record = request.get_json()
    project = ProjectSchema().load(record)

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO projects (project_name) VALUES (%s) RETURNING project_id',
                        (project.project_name,))

            project_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({"project_id" : project_id})
    
@blueprint.route('/v1/projects', methods=["GET"])
def list_projects():
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT project_id, project_name FROM projects")
            
            projects = []
            for _id, _name in cur:
                project = {
                    "project_id" : _id,
                    "project_name" : _name
                }
                
                projects.append(project)

    conn.commit()
    conn.close()

    return jsonify({"projects" : projects})
    
@blueprint.route('/v1/projects/<int:project_id>', methods=["GET"])
def get_project(project_id):
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT project_id, project_name FROM projects "
                        "WHERE project_id = %s",
                        (project_id,))
            
            _id, _name = cur.fetchone()
            
            project = {
                "project_id" : _id,
                "project_name" : _name
            }

    conn.commit()
    conn.close()

    return jsonify(project)
