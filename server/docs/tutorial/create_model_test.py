"""
Run tests on a Ringling model and put the results back
"""
import datetime
import pickle
import requests
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score


# Set the endpoint url for parameter set creation
BASE_URL = "http://localhost:8888"
MODEL_URL = "/v1/trained_models"
MODEL_TEST_URL = "/v1/model_tests"
MODEL_REQUEST_URL = BASE_URL + MODEL_URL
MODEL_TEST_REQUEST_URL = BASE_URL + MODEL_TEST_URL


# Set this to the ID of the project you created earlier
PROJECT_ID = 3

# Set this to the ID of the parameter set you created earlier
PARAMETER_SET_ID = 9

# Set this to the ID of the trained model you created earlier
TRAINED_MODEL_ID = 8

# Send the request, get the pickled trained model, and unpickle it
REQUEST_URL = MODEL_REQUEST_URL + "/" + str(TRAINED_MODEL_ID)
response = requests.get(REQUEST_URL, timeout=5)
pickled_model = response.json()["model_object"]
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

response = requests.post(MODEL_TEST_REQUEST_URL, json=test_payload, timeout=5)

# Make sure it worked
print(response.json())
