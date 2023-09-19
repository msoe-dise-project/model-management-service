"""
Create a new project to import into ringling
"""
import requests

# Set the endpoint url for project creation
BASE_URL = "http://localhost:8888"
OBJECT_URL = "/v1/projects"
REQUEST_URL = BASE_URL + OBJECT_URL

name_payload = {"project_name": "Tutorial Project"}

# Create the project
response = requests.post(REQUEST_URL,
                         json=name_payload, timeout=5)

# Make sure it worked
print(response.json())
