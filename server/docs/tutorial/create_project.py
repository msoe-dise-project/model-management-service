import requests

# Set the endpoint url for project creation
base_url = "http://localhost:8888"
object_url = "/v1/projects"
request_url = base_url + object_url

name_payload = {"project_name": "Tutorial Project"}

# Create the project
response = requests.post(request_url,
                         json=name_payload, timeout=5)

# Make sure it worked
print(response.json())
