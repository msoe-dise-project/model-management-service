"""
Create a new project to import into ringling
"""
import requests
from ringling_lib.ringling_db import RinglingDBSession
from ringling_lib.project import Project

# Set the endpoint url for project creation
BASE_URL = "http://localhost:8888"

PROJECT_NAME = "Tutorial Project"
metadata = {"info1": "This is the Tutorial Project"}

# Create the project
project_payload = Project(PROJECT_NAME, metadata)

# Create an instance of RinglingDB and send the project
session = RinglingDBSession(BASE_URL)
cur_id = session.create_project(project_payload)

# Make sure it worked
if cur_id is None:
    print(f"Project with name {PROJECT_NAME} already exists")
else:
    print(f"New Project created with ID {cur_id}")
