"""
Create a parameter set as a serialized Scikit-learn pipeline and put it into Ringling
"""
import pickle
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from ringling_lib.ringling_db import RinglingDBSession
from ringling_lib.param_set import ParameterSet

# Set the endpoint url for parameter set creation
BASE_URL = "http://localhost:8888"
metadata = {"info2": "This is the Tutorial Parameter Set"}

# Set this to the project ID of the project you created earlier
PROJECT_ID = 3

# Create the pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

# Convert pipeline to a hexed pickle to store it as a string
pickled_pipeline = pickle.dumps(pipeline).hex()

param_payload = ParameterSet(PROJECT_ID,
                             pickled_pipeline,
                             True,
                             metadata)

# Create an instance of RinglingDB and create the parameter set
session = RinglingDBSession(BASE_URL)
cur_id = session.create_param_set(param_payload)

# Make sure it worked
print(f"New Parameter Set created with ID {cur_id}")
