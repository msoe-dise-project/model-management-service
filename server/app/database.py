"""
Database helper methods
"""

import os
import sys

DATABASE_KEY = "POSTGRES_DATABASE"
HOST_KEY = "POSTGRES_HOST"
USERNAME_KEY = "POSTGRES_USERNAME"
PASSWORD_KEY = "POSTGRES_PASSWORD"
PORT_KEY = "POSTGRES_PORT"
DEFAULT_PORT = 5432
DEFAULT_DATABASE = "model_management_service"

def check_environment_parameters():
    """
    Checks if host, username, and password environment variables were set up correctly
    :return: None
    """
    if HOST_KEY not in os.environ or \
       USERNAME_KEY not in os.environ or \
       PASSWORD_KEY not in os.environ:
        msg = f"Must specify environmental variables {HOST_KEY}, " \
              f"{USERNAME_KEY}, and {PASSWORD_KEY}."
        print(msg, file=sys.stderr)
        sys.exit(1)

def get_database_uri():
    """
    Get the URI for the database
    :return: URI
    """
    uri = f"postgresql://{os.environ.get(USERNAME_KEY)}:{os.environ.get(PASSWORD_KEY)}" \
          f"@{os.environ.get(HOST_KEY)}:{os.environ.get(PORT_KEY, DEFAULT_PORT)}" \
          f"/{os.environ.get(DATABASE_KEY, DEFAULT_DATABASE)}"

    return uri
