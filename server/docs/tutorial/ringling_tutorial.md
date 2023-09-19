# Using Ringling

Ringling is a service that offers the ability to manage projects, parameter sets, models, and tests. This allows for an integrated workflow from the creation of a model, to its deployment. The following is a brief overview of the different parts:

| Object Type   | Description                                           | Belongs in    |
|---------------|-------------------------------------------------------|---------------|
| Project       | Manage projects as a whole                            | Top Level     |
| Parameter Set | Untrained models, pickled or json                     | Project       |
| Trained Model | Trained model with deploy status and backtest metrics | Parameter Set |
| Model Test    | Model test to check for data drift                    | Trained Model |

## Creating a Project
The following is the schema for Projects:

| Object Name              | Object Type |
|--------------------------|-------------|
| project_id (Primary Key) | Integer     |
| project_name             | String      |

The first step of interacting with Ringling is to create a project. First, make sure [Ringling](https://github.com/msoe-dise-project/ringling) is running.

This can be done in two ways:

#### Python:
```python
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
```

If everything is successful, this should output:
```bash
{'project_id': 3}
```



#### Ringling-cli
Some of the steps in this tutorial can also be performed using [Ringling-cli](https://github.com/msoe-dise-project/ringling-cli)

Input:
```bash
ringling-cli localhost project create --name "tutorial"
```

Output:
```
Project tutorial created successfully
Project ID: 5
```




## Creating a Parameter Set
The following is the schema for Parameter Sets:

| Object Name                    | Object Type     |
|--------------------------------|-----------------|
| project_id                     | Integer         |
| parameter_set_id (Primary Key) | Integer         |
| training_parameters            | Hex Byte String |
| is_active                      | Boolean         |
Now that there is a project, an untrained model, or parameter set, should be created. For this example, we are using a Scikit-learn Pipeline that includes a standard scaler and logistic regression. 

```python
"""
Create a parameter set as a serialized Scikit-learn pipeline and put it into ringling
"""
import pickle
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

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

```

This should output (but potentially with a different ID):
```bash
{'parameter_set_id': 9}
```

Now that we have created a parameter set, let's use Ringling-cli to see its data.

Input:
```bash
ringling-cli localhost param-set get --id 9
```

Output (training_parameters field shortened for clarity):
```bash
{'is_active': True,
 'parameter_set_id': 9,
 'project_id': 3,
 'training_parameters': '800495f6010000000000008c10736b6c6561726e2e706970656c6...'}
 ```

## Training and Backtesting a Model
The following is the schema for Trained Models:

| Object Name            | Object Type                                           |
|------------------------|-------------------------------------------------------|
| project_id             | Integer                                               |
| parameter_set_id       | Integer                                               |
| model_id (Primary Key) | Integer                                               |
| training_data_from     | ISO 8601 Date Format                                  |
| training_data_until    | ISO 8601 Date Format                                  |
| model_object           | Hex Byte String                                       |
| train_timestamp        | ISO 8601 Date Format                                  |
| deployment_stage       | String (Can be "testing", "production", or "retired") |
| backtest_timestamp     | ISO 8601 Date Format                                  |
| backtest_metrics       | JSONB                                                 |
| passed_backtesting     | Boolean                                               |
In this example, the pipeline is retrieved from Ringling. Then, it is evaluated using time based K-fold cross validation, before being trained on all available data and saved back to ringling as a Trained Model with its backtest metrics.

```python
"""
Train a model given a parameter set in Ringling
"""
import datetime
import pickle
import numpy as np
import requests
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split


# Set the endpoint url for parameter set get, and trained model create
BASE_URL = "http://localhost:8888"
PARAM_URL = "/v1/parameter_sets"
MODEL_URL = "/v1/trained_models"
PARAM_REQUEST_URL = BASE_URL + PARAM_URL
MODEL_REQUEST_URL = BASE_URL + MODEL_URL

# Set this to the ID of the project you created earlier
PROJECT_ID = 3

# Set this to the ID of the parameter set you created earlier
PARAMETER_SET_ID = 9

# Send the request, get the pickled parameter set
request_url = PARAM_REQUEST_URL + "/" + str(PARAMETER_SET_ID)
response = requests.get(request_url, timeout=5)
pickled_pipeline = response.json()["training_parameters"]

pipeline = pickle.loads(bytes.fromhex(pickled_pipeline))

# Load in the training data from the heart disease dataset, and split it
# Retrieved from: https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
df = pd.read_csv("heart_train.csv")
X = df.drop("target", axis=1)
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the model, and get timestamp
train_timestamp = datetime.datetime.now().isoformat()

# Time based cross validation
# Please note that while this dataset does not indicate times, the following algorithm
# can be used assuming the dataframe is sorted by time to generate test metrics

K_SPLITS = 5
vals = len(X)
partition = vals // K_SPLITS

accuracies = np.zeros(K_SPLITS - 1)
precisions = np.zeros(K_SPLITS - 1)
recalls = np.zeros(K_SPLITS - 1)
areas_under_roc = np.zeros(K_SPLITS - 1)

for split in range(1, K_SPLITS):
    train_end = partition*split
    test_end = partition*(split+1)
    X_train = X.head(train_end)
    y_train = y.head(train_end)
    X_test = X.loc[train_end:test_end]
    y_test = y.loc[train_end:test_end]
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracies[split-1] = accuracy_score(y_test, y_pred)
    precisions[split-1] = precision_score(y_test, y_pred)
    recalls[split-1] = recall_score(y_test, y_pred)
    areas_under_roc[split-1] = roc_auc_score(y_test, y_pred)

test_timestamp = datetime.datetime.now().isoformat()

# Get summary statistics of all metrics generated by time based CV
accuracy = np.mean(accuracies)
accuracy_std = np.std(accuracies)
precision = np.mean(precisions)
precision_std = np.std(precisions)
recall = np.mean(recalls)
recall_std = np.std(recalls)
area_under_roc = np.mean(areas_under_roc)
area_under_roc_std = np.std(areas_under_roc)

print(f"Accuracy: {accuracy:.5f}")
print(f"Accuracy Standard Deviation: {accuracy_std:.5f}")
print(f"Precision: {precision:.5f}")
print(f"Precision Standard Deviation: {precision_std:.5f}")
print(f"Recall: {recall:.5f}")
print(f"Recall Standard Deviation: {recall_std:.5f}")
print(f"AUROC: {area_under_roc:.5f}")
print(f"AUROC Standard Deviation: {area_under_roc_std:.5f}")

passed_testing = bool(area_under_roc > 0.8)

# Prepare metrics to be sent to Ringling
test_metrics = {
    "accuracy" : accuracy,
    "accuracy_std" : accuracy_std,
    "precision" : precision,
    "precision_std" : precision_std,
    "recall" : recall,
    "recall_std" : recall_std,
    "auroc" : area_under_roc,
    "auroc_std" : area_under_roc_std
}

# Now that we have validation metrics, train the model on all available data
pipeline.fit(X, y)
pipeline_object = pickle.dumps(pipeline).hex()

# Save the model to Ringling
model_payload = {"project_id": PROJECT_ID,
                 "parameter_set_id": PARAMETER_SET_ID,
                 "training_data_from": "1988-01-01T00:00:00.000000",
                 "training_data_until": "1988-12-31T23:59:59.999999",
                 "model_object": pipeline_object,
                 "train_timestamp": train_timestamp,
                 "deployment_stage": "testing",
                 "backtest_timestamp": test_timestamp,
                 "backtest_metrics": test_metrics,
                 "passed_backtesting": passed_testing}

response = requests.post(MODEL_REQUEST_URL, json=model_payload, timeout=5)

# Make sure it worked
print(response.json())
```

This should output:
```bash
Accuracy: 0.85061
Accuracy Standard Deviation: 0.01952
Precision: 0.83772
Precision Standard Deviation: 0.03900
Recall: 0.88678
Recall Standard Deviation: 0.01711
AUROC: 0.85007
AUROC Standard Deviation: 0.01981
{'model_id': 8}
```

Now, let's see the model object it created using Ringling-cli
```bash
ringling-cli localhost trained-model get --id 8
```

Output (model_object field shortened for clarity):
```bash
{'backtest_metrics': {'accuracy': 0.850609756097561,
                      'accuracy_std': 0.019521720236075776,
                      'auroc': 0.8500733994974246,
                      'auroc_std': 0.01980587001464519,
                      'precision': 0.8377163295641556,
                      'precision_std': 0.038996281267517356,
                      'recall': 0.8867752114448577,
                      'recall_std': 0.017109439332137488},
 'backtest_timestamp': '2023-08-15T12:10:55.438305',
 'deployment_stage': 'testing',
 'model_id': 8,
 'model_object': '80049576060000000000008c10...',
 'parameter_set_id': 9,
 'passed_backtesting': True,
 'project_id': 3,
 'train_timestamp': '2023-08-15T12:10:55.384296',
 'training_data_from': '1988-01-01T00:00:00',
 'training_data_until': '1988-12-31T23:59:59.999999'}
 ```

## Testing the Model on Unseen Data
The following is the schema for Model Tests:

| Object Name      | Object Type            |
|------------------|------------------------|
| project_id       | Integer                |
| parameter_set_id | Integer                |
| model_id         | Integer                |
| test_id          | Integer  (Primary Key) |
| test_timestamp   | ISO 8601 Date Format   |
| test_metrics     | JSONB                  |
| passed_testing   | Boolean                |

In this example, the model is retrieved from Ringling. Then, it is evaluated the test set before saved back to ringling as a Model Test with its test metrics.
```python
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
request_url = MODEL_REQUEST_URL + "/" + str(TRAINED_MODEL_ID)
response = requests.get(request_url, timeout=5)
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
```

This should output:
```bash
Accuracy: 0.80583
Precision: 0.77064
Recall: 0.84848
AUROC: 0.80742
{'test_id': 6}
```

Now, let's see the model test it created using Ringling-cli:
```bash
ringling-cli localhost model-test get --id 6
```

Output:
```bash
{'model_id': 8,
 'parameter_set_id': 9,
 'passed_testing': True,
 'project_id': 3,
 'test_id': 6,
 'test_metrics': {'accuracy': 0.8058252427184466,
                  'auroc': 0.8074199943358822,
                  'precision': 0.7706422018348624,
                  'recall': 0.8484848484848485},
 'test_timestamp': '2023-08-15T12:37:35.950711'}
 ```

## Wrap Up
And there we have it! In this tutorial, we first created an empty project. Then, we created a parameter set as a pickled, untrained Scikit-learn pipeline. Afterwards, we retrieved it from Ringling and trained it on some data, as well performed backtesting before saving it as a trained model object. Finally, we pulled it and tested it on some entirely unseen data and saved the test metrics as a model test object in Ringling.