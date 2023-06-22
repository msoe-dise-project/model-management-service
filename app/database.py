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
    if HOST_KEY not in os.environ or \
       USERNAME_KEY not in os.environ or \
       PASSWORD_KEY not in os.environ:
        msg = "Must specify environmental variables {}, {}, and {}.".format(HOST_KEY, USERNAME_KEY, PASSWORD_KEY)
        print(msg, file=sys.stderr)
        sys.exit(1)
        
def get_database_uri():
    uri = "postgresql://{}:{}@{}:{}/{}".format(os.environ.get(USERNAME_KEY),
                                               os.environ.get(PASSWORD_KEY),
                                               os.environ.get(HOST_KEY),
                                               os.environ.get(PORT_KEY, DEFAULT_PORT),
                                               os.environ.get(DATABASE_KEY, DEFAULT_DATABASE))
    
    return uri
