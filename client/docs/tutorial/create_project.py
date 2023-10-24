"""
Create a new project to import into ringling
"""
import requests
from ringling_lib.ringling_db import RinglingDBSession
from ringling_lib.project import Project

# Set the endpoint url for project creation
BASE_URL = "http://localhost:8888"

project_name = "Tutorial Project"
metadata = {"info1": "This is the Tutorial Project"}

# Create the project
project_payload = Project(project_name, metadata)

# Create an instance of RinglingDB and send the project
session = RinglingDBSession(BASE_URL)
cur_id = session.create_project(project_payload)

# Make sure it worked
if cur_id is None:
    print(f"Project with name {project_name} already exists")
else:
    print(f"New Project created with ID {cur_id}")
