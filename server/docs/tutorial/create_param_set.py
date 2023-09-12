"""
Create a parameter set as a serialized Scikit-learn pipeline and put it into ringling
"""
import pickle
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Set the endpoint url for parameter set creation
BASE_URL = "http://localhost:8888"
OBJECT_URL = "/v1/parameter_sets"
REQUEST_URL = BASE_URL + OBJECT_URL

# Set this to the project ID of the project you created earlier
PROJECT_ID = 3

# Create the pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

# Convert pipeline to a hexed pickle to store it as a string
pickled_pipeline = pickle.dumps(pipeline).hex()

param_payload = {"project_id": PROJECT_ID,
                 "training_parameters": pickled_pipeline,
                 "is_active": True}

# Create the parameter set
response = requests.post(REQUEST_URL, json=param_payload, timeout=5)

# Make sure it worked
print(response.json())
