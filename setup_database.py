#!/usr/bin/env python

import os
import sys

import psycopg2

HOST_KEY = "POSTGRES_HOST"
USER_PASSWORD_KEY = "POSTGRES_USER_PASSWORD"
ADMIN_PASSWORD_KEY = "POSTGRES_ADMIN_PASSWORD"

PORT_KEY = "POSTGRES_PORT"
DEFAULT_PORT = 5432

ADMIN_DATABASE = "postgres"
ADMIN_USER = "postgres"
SERVICE_USER = "model_management_service"

DATABASE_NAME = "model_management_service"

if __name__ == "__main__":
    for key in [HOST_KEY, USER_PASSWORD_KEY, ADMIN_PASSWORD_KEY]:
        if key not in os.environ:
            msg = "Must specify environmental variable {}".format(key)
            print(msg)
            sys.exit(1)

    admin_uri = "postgresql://{}:{}@{}:{}/{}".format(ADMIN_USER,
                                               os.environ.get(ADMIN_PASSWORD_KEY),
                                               os.environ.get(HOST_KEY),
                                               os.environ.get(PORT_KEY, DEFAULT_PORT),
                                               ADMIN_DATABASE)

    with psycopg2.connect(admin_uri) as conn:
        with conn.cursor() as cur:
            # need to disable transactions to create / remove databases
            cur.execute("ABORT TRANSACTION;")
            # I tried using SQL parameters but psycopg2 quotes the strings
            cur.execute("DROP DATABASE IF EXISTS {};".format(DATABASE_NAME))
            cur.execute("CREATE DATABASE {};".format(DATABASE_NAME))
    conn.close()

    database_uri = "postgresql://{}:{}@{}:{}/{}".format(ADMIN_USER,
                                                   os.environ.get(ADMIN_PASSWORD_KEY),
                                                   os.environ.get(HOST_KEY),
                                                   os.environ.get(PORT_KEY, DEFAULT_PORT),
                                                   DATABASE_NAME)

    with psycopg2.connect(database_uri) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS projects;")

            cur.execute("CREATE TABLE projects ("
                        "project_id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY, "
                        "project_name text NOT NULL, "
                        "project_start timestamp NOT NULL, "
                        # nullable on purpose for indefinite configurations
                        "project_end timestamp "
                        ");")
            
            cur.execute("DROP TABLE IF EXISTS parameter_sets;")

            cur.execute("CREATE TABLE parameter_sets ( "
                        "parameter_set_id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY, "
                        "project_id integer NOT NULL, "
                        "parameters jsonb NOT NULL, "
                        # nullable on purpose for inactive or indefinite configurations
                        "active_from timestamp, "
                        "active_until timestamp "
                        ");")

            cur.execute("DROP TABLE IF EXISTS trained_models;")

            cur.execute("CREATE TABLE trained_models ( "
                        "model_id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY, "
                        "project_id integer NOT NULL, "
                        "parameter_set_id integer NOT NULL, "
                        "training_data_from timestamp NOT NULL, "
                        "training_data_until timestamp NOT NULL, "
                        # serialized objects are stored as hex string representations of bytes objects
                        "model_object text NOT NULL, "
                        "train_timestamp timestamp NOT NULL, "
                        # nullable on purpose for inactive or indefinite configurations
                        "active_from timestamp, "
                        "active_until timestamp "
                        ");")
                        
            cur.execute("DROP TABLE IF EXISTS model_tests;")

            cur.execute("CREATE TABLE model_tests ( "
                        "test_id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY, "
                        "project_id integer NOT NULL, "
                        "parameter_set_id integer NOT NULL, "
                        "model_id integer NOT NULL, "
                        "test_timestamp timestamp NOT NULL, "
                        "test_metrics jsonb NOT NULL, "
                        "passed_testing bool NOT NULL "
                        ");")

            cur.execute("DROP ROLE IF EXISTS {};".format(SERVICE_USER))
            cur.execute("CREATE USER {} WITH PASSWORD '{}';".format(SERVICE_USER,
                                                            os.environ.get(USER_PASSWORD_KEY)))
            cur.execute("GRANT SELECT, INSERT, UPDATE ON projects TO {};".format(SERVICE_USER))
            cur.execute("GRANT SELECT, INSERT, UPDATE ON parameter_sets TO {};".format(SERVICE_USER))
            cur.execute("GRANT SELECT, INSERT, UPDATE ON trained_models TO {};".format(SERVICE_USER))
            cur.execute("GRANT SELECT, INSERT, UPDATE ON model_tests TO {};".format(SERVICE_USER))

        conn.commit()

    conn.close()
