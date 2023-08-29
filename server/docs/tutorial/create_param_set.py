import pickle
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Set the endpoint url for parameter set creation
base_url = "http://localhost:8888"
object_url = "/v1/parameter_sets"
request_url = base_url + object_url

# Set this to the project ID of the project you created earlier
project_id = 3

# Create the pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

# Convert pipeline to a hexed pickle to store it as a string
pickled_pipeline = pickle.dumps(pipeline).hex()

param_payload = {"project_id": project_id,
                 "training_parameters": pickled_pipeline,
                 "is_active": True}

# Create the parameter set
response = requests.post(request_url,
                         json=param_payload)

# Make sure it worked
print(response.json())
