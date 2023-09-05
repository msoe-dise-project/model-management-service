import argparse
import datetime as dt
import pickle
import os
import sys
import unittest

import requests

BASE_URL_KEY = "BASE_URL"

class TrainedModelTests(unittest.TestCase):
    def get_url(self):
        return os.path.join(os.environ[BASE_URL_KEY], "v1/trained_models")

    def test_create_success(self):
        test_model = set([1, 3, 5])
        
        obj = { "project_id" : 5,
                "parameter_set_id" : 1,
                "training_data_from" : (dt.datetime.now() - dt.timedelta(days=3)).isoformat(),
                "training_data_until" : dt.datetime.now().isoformat(),
                "model_object" : pickle.dumps(test_model).hex(),
                "train_timestamp" : dt.datetime.now().isoformat(),
                "deployment_stage" : "testing",
                "backtest_timestamp": dt.datetime.now().isoformat(),
                "backtest_metrics": {"recall": 0.8, "precision": 0.2},
                "passed_backtesting": True
        }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        self.assertIn("model_id", json_response)
        self.assertIsInstance(json_response["model_id"], int)
        
    def test_create_success_bad_schema(self):
        test_model = set([1, 3, 5])
        
        obj = { "not_a_project_id" : 5,
                "what's a parameter set?" : 1,
                "training_data_from" : "last year",
                "training_data_until" : "last month",
                "model_object" : pickle.dumps(test_model).hex(),
                "train_timestamp" : "today",
                "deployment_stage" : "testing",
                "we're testing now?": dt.datetime.now().isoformat(),
                "test_metrics": {"recall": 0.8, "precision": 0.2},
                "passed_testing": True
        }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 400)
        
    def test_list_models(self):
        test_model1 = set([1, 3, 5])
        
        obj1 = { "project_id" : 5,
                 "parameter_set_id" : 1,
                 "training_data_from" : (dt.datetime.now() - dt.timedelta(days=3)).isoformat(),
                 "training_data_until" : dt.datetime.now().isoformat(),
                 "model_object" : pickle.dumps(test_model1).hex(),
                 "train_timestamp" : dt.datetime.now().isoformat(),
                 "deployment_stage" : "testing",
                 "backtest_timestamp": dt.datetime.now().isoformat(),
                 "backtest_metrics": {"recall": 0.8, "precision": 0.2},
                 "passed_backtesting": True
        }
                 
        response = requests.post(self.get_url(),
                            json=obj1)

        self.assertEqual(response.status_code, 201)

        test_model2 = set([5, 21, 13])
        obj2 = { "project_id" : 5,
                 "parameter_set_id" : 2,
                 "training_data_from" : (dt.datetime.now() - dt.timedelta(days=3)).isoformat(),
                 "training_data_until" : dt.datetime.now().isoformat(),
                 "model_object" : pickle.dumps(test_model2).hex(),
                 "train_timestamp" : dt.datetime.now().isoformat(),
                 "deployment_stage" : "testing",
                 "backtest_timestamp": dt.datetime.now().isoformat(),
                 "backtest_metrics": {"recall": 0.7, "precision": 0.3},
                 "passed_backtesting": True
        }
                 
        response = requests.post(self.get_url(),
                            json=obj2)

        self.assertEqual(response.status_code, 201)

        test_model3 = set([5, 21, 13])
        obj3 = { "project_id" : 5,
                 "parameter_set_id" : 3,
                 "training_data_from" : (dt.datetime.now() - dt.timedelta(days=3)).isoformat(),
                 "training_data_until" : dt.datetime.now().isoformat(),
                 "model_object" : pickle.dumps(test_model3).hex(),
                 "train_timestamp" : dt.datetime.now().isoformat(),
                 "deployment_stage" : "testing",
                 "backtest_timestamp": dt.datetime.now().isoformat(),
                 "backtest_metrics": {"recall": 0.9, "precision": 0.1},
                 "passed_backtesting": True
        }
                 
        response = requests.post(self.get_url(),
                            json=obj3)

        self.assertEqual(response.status_code, 201)

        response = requests.get(self.get_url())
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertIn("trained_models", json_response)
        self.assertGreaterEqual(len(json_response["trained_models"]), 3)
        
    def test_get_model_by_id(self):
        test_model = set([5, 21, 13])
        obj1 = { "project_id" : 5,
                 "parameter_set_id" : 49,
                 "training_data_from" : (dt.datetime.now() - dt.timedelta(days=3)).isoformat(),
                 "training_data_until" : dt.datetime.now().isoformat(),
                 "model_object" : pickle.dumps(test_model).hex(),
                 "train_timestamp" : dt.datetime.now().isoformat(),
                 "deployment_stage" : "testing",
                 "backtest_timestamp": dt.datetime.now().isoformat(),
                 "backtest_metrics": {"recall": 0.8, "precision": 0.2},
                 "passed_backtesting": True
        }

        response = requests.post(self.get_url(),
                            json=obj1)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        model_id = json_response["model_id"]
        
        url = os.path.join(self.get_url(), str(model_id))
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        unpickled_model = pickle.loads(bytes.fromhex(json_response["model_object"]))
        self.assertEqual(test_model, unpickled_model)

    def test_get_model_by_bad_id(self):
        model_id = 0

        url = os.path.join(self.get_url(), str(model_id))

        response = requests.get(url)
        self.assertEqual(response.status_code, 404)

        json_obj = response.json()
        self.assertIn("error", json_obj)

    def test_model_status_update(self):
        test_model = set([5, 21, 13])
        obj1 = { "project_id" : 5,
                 "parameter_set_id" : 49,
                 "training_data_from" : (dt.datetime.now() - dt.timedelta(days=3)).isoformat(),
                 "training_data_until" : dt.datetime.now().isoformat(),
                 "model_object" : pickle.dumps(test_model).hex(),
                 "train_timestamp" : dt.datetime.now().isoformat(),
                 "deployment_stage" : "testing",
                 "backtest_timestamp": dt.datetime.now().isoformat(),
                 "backtest_metrics": {"recall": 0.8, "precision": 0.2},
                 "passed_backtesting": True
        }

        response = requests.post(self.get_url(),
                            json=obj1)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        model_id = json_response["model_id"]
        
        patch = {
            "deployment_stage" : "production"
        }
        
        url = os.path.join(self.get_url(), str(model_id))
        response = requests.patch(url, json=patch)

        self.assertEqual(response.status_code, 200)
        
        patch = {
            "deployment_stage" : "retired"
        }
        
        url = os.path.join(self.get_url(), str(model_id))
        response = requests.patch(url, json=patch)

        self.assertEqual(response.status_code, 200)
        
    def test_model_status_update_bad_schema(self):
        test_model = set([5, 21, 13])
        obj1 = { "project_id" : 5,
                 "parameter_set_id" : 49,
                 "training_data_from" : (dt.datetime.now() - dt.timedelta(days=3)).isoformat(),
                 "training_data_until" : dt.datetime.now().isoformat(),
                 "model_object" : pickle.dumps(test_model).hex(),
                 "train_timestamp" : dt.datetime.now().isoformat(),
                 "deployment_stage" : "testing",
                 "backtest_timestamp": dt.datetime.now().isoformat(),
                 "backtest_metrics": {"recall": 0.8, "precision": 0.2},
                 "passed_backtesting": True
        }

        response = requests.post(self.get_url(),
                            json=obj1)

        self.assertEqual(response.status_code, 201)

        json_response = response.json()

        model_id = json_response["model_id"]
        
        patch = {
            "not a valid field" : "production"
        }
        
        url = os.path.join(self.get_url(), str(model_id))
        response = requests.patch(url, json=patch)

        self.assertEqual(response.status_code, 400)

    def test_model_status_update_bad_id(self):
        model_id = 0

        url = os.path.join(self.get_url(),
                           str(model_id))

        update = {"deployment_stage" : "retired"}

        response = requests.patch(url, json=update)

        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    if BASE_URL_KEY not in os.environ:
        print("Must define the base URL using the {} environment variable".format(BASE_URL_KEY))
        sys.exit(1)

    unittest.main()