"""
Run tests on a Ringling model and put the results back
"""
import datetime
import pickle
import requests
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from ringling_lib.ringling_db import RinglingDBSession
from ringling_lib.trained_model import TrainedModel
from ringling_lib.model_test import ModelTest


# Set the endpoint url for parameter set creation
BASE_URL = "http://localhost:8888"
metadata = {"info4": "This is the Tutorial Model Test"}

# Set this to the ID of the project you created earlier
PROJECT_ID = 3

# Set this to the ID of the parameter set you created earlier
PARAMETER_SET_ID = 9

# Set this to the ID of the trained model you created earlier
TRAINED_MODEL_ID = 8

# Create an instance of RinglingDB and retrieve the trained model
session = RinglingDBSession(BASE_URL)
trained_model = session.get_trained_model(TRAINED_MODEL_ID)
pickled_model = trained_model.model_object
model = pickle.loads(bytes.fromhex(pickled_model))

# Load unseen test data
df = pd.read_csv("heart_test.csv")
X_test = df.drop("target", axis=1)
y_test = df["target"]
y_pred = model.predict(X_test)

# Get test metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
area_under_roc = roc_auc_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.5f}")
print(f"Precision: {precision:.5f}")
print(f"Recall: {recall:.5f}")
print(f"AUROC: {area_under_roc:.5f}")

test_metrics = {
    "accuracy" : accuracy,
    "precision" : precision,
    "recall" : recall,
    "auroc" : area_under_roc,
}

test_timestamp = datetime.datetime.now().isoformat()
passed_testing = bool(area_under_roc > 0.8)

# Save the model to Ringling
test_payload = {"project_id": PROJECT_ID,
                "parameter_set_id": PARAMETER_SET_ID,
                "model_id": TRAINED_MODEL_ID,
                "test_timestamp": test_timestamp,
                "test_metrics": test_metrics,
                "passed_testing": passed_testing}

model_test_payload = ModelTest(PROJECT_ID,
                               PARAMETER_SET_ID,
                               TRAINED_MODEL_ID,
                               test_timestamp,
                               test_metrics,
                               passed_testing,
                               metadata)

cur_id = session.create_model_test(model_test_payload)

# Make sure it worked
print(f"New Model Test created with ID {cur_id}")
