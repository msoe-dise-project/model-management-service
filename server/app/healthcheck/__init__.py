"""
The healthcheck module
Used to test if there is a successful connection to Ringling, and that all tables are healthy
"""
from flask import Blueprint

from flask import request
from flask.json import jsonify

import psycopg2

from app.database import get_database_uri

blueprint = Blueprint("healthcheck", __name__)

@blueprint.route("/healthcheck", methods=["GET"])
def healthcheck():
    """
    Perform a healthcheck on the database
    :return: Jsonified healthcheck results, the status code of the request
    """
    failure_occurred = False
    successful_connection = False
    successful_queries = []

    tables = ["model_tests", "parameter_sets", "projects", "trained_models"]

    try:
        uri = get_database_uri()
        with psycopg2.connect(uri) as conn:
            with conn.cursor() as cur:
                successful_connection = True

                for table in tables:
                    print("SELECT count(*) FROM {}".format(table))
                    cur.execute("SELECT count(*) FROM %s", table)
                    cur.fetchone()[0]
                    successful_queries.append(table)

                successful_queries = True

        conn.close()
    except:
        failure_occurred = True

    status_code = 200
    if failure_occurred:
        status_code = 500

    obj = {
        "database" :
        {
            "healthy" : failure_occurred,

            "connection" :
            {
                "healthy" : successful_connection
            },

            "tables" :
            {
                "healthy" : len(successful_queries) == len(tables),
                "successful_queries" : successful_queries
            }
        }
    }

    return jsonify(obj), status_code
