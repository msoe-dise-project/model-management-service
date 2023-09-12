"""
The project module
Used to perform actions with regard to Ringling projects
"""

from flask import Blueprint

import datetime as dt

from flask import request
from flask.json import jsonify

import psycopg2
from psycopg2.extras import Json

from app.database import get_database_uri
from app.schemas import Project
from app.schemas import ProjectSchema
from app.schemas import ValidationError

blueprint = Blueprint("projects", __name__)

@blueprint.route('/v1/projects', methods=["POST"])
def create_project():
    """
    Create a new project in Ringling
    :return: The ID of the newly created project, status code
    """
    try:
        record = request.get_json()
        project = ProjectSchema().load(record)
    except ValidationError as err:
        return jsonify(err.messages), 400

    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute(f'SELECT project_name FROM projects '
                        f'WHERE project_name=\'{project.project_name}\' LIMIT 1')
            result = cur.fetchone()
            if result is not None:
                return jsonify({"error": f"Project {project.project_name} already exists"}), 400
            cur.execute('INSERT INTO projects (project_name) VALUES (%s) RETURNING project_id',
                        (project.project_name,))
            project_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({"project_id" : project_id}), 201

@blueprint.route('/v1/projects', methods=["GET"])
def list_projects():
    """
    Retrieve all projects from Ringling
    :return: The projects as a JSON object
    """
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT project_id, project_name FROM projects")

            projects = [
                Project(_name, _id) \
                for _id, _name in cur
            ]

    conn.commit()
    conn.close()

    return jsonify({"projects" : projects})

@blueprint.route('/v1/projects/<int:project_id>', methods=["GET"])
def get_project(project_id):
    """
    Retrieve a project from Ringling by ID
    :param project_id: The project ID to retrieve
    :return: the project as a JSON object
    """
    uri = get_database_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT project_id, project_name FROM projects "
                        "WHERE project_id = %s",
                        (project_id,))
            result = cur.fetchone()
            if result is None:
                return jsonify({"error": f"ID {project_id} not found"}), 404
            _id, _name = result
            project = Project(_name, _id)

    conn.commit()
    conn.close()

    return jsonify(project)
