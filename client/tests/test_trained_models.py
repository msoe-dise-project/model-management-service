"""
Copyright 2023 MSOE DISE Project
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import unittest
from datetime import datetime

from ringling_lib.trained_model import TrainedModel
from ringling_lib.ringling_db import RinglingDBSession

BASE_URL_KEY = "RINGLING_BASE_URL"
base_url = os.environ.get(BASE_URL_KEY)

class TestTrainedModels(unittest.TestCase):
    """
    Test interacting with Trained Models
    """
    def test_trained_model_create_dict(self):
        """
        Create a trained model using dictionary values
        :return: If the trained model was created successfully
        """
        session = RinglingDBSession(base_url)
        obj = {"project_id": 3,
                 "parameter_set_id": 2,
                 "training_data_from": "1995-01-01T00:00:00.000000",
                 "training_data_until": "2000-12-31T23:59:59.999999",
                 "model_object": "0x00a5234f6123371",
                 "train_timestamp": datetime.now().isoformat(),
                 "deployment_stage": "testing",
                 "backtest_timestamp": datetime.now().isoformat(),
                 "backtest_metrics": {"precision": 0.85, "recall": 0.75},
                 "passed_backtesting": True,
                 "metadata": {"Additional data":"More data"}}
        test_trained_model = TrainedModel(
                obj['project_id'],
                obj['parameter_set_id'],
                obj['training_data_from'],
                obj['training_data_until'],
                obj['model_object'],
                obj['train_timestamp'],
                obj['deployment_stage'],
                obj['backtest_timestamp'],
                obj['backtest_metrics'],
                obj['passed_backtesting'],
                obj['metadata']
        )
        trained_model_id = session.create_trained_model(test_trained_model)
        self.assertIsInstance(trained_model_id, int)

    def test_trained_model_create_direct(self):
        """
        Create a trained model using direct values
        :return: If the trained model was created successfully
        """
        session = RinglingDBSession(base_url)
        test_trained_model = TrainedModel(
            1,5, "1998-01-01T00:00:00.000000", "2005-12-31T23:59:59.999999",
            "0x00a5234f61634236", datetime.now().isoformat(), "testing",
            datetime.now().isoformat(), {"precision": 0.85, "recall": 0.75},
            True, {"Additional data":"Even more data"}
        )
        trained_model_id = session.create_trained_model(test_trained_model)
        self.assertIsInstance(trained_model_id, int)

    def test_trained_model_get(self):
        """
        Get a trained model given an ID
        :return: If the retrieved trained model object and backtest timestamp match the ones sent
        """
        session = RinglingDBSession(base_url)
        test_trained_model = TrainedModel(
            1,5, "2010-01-01T00:00:00.000000", "2015-12-31T23:59:59.999999",
            "0x00a5234f6733135", datetime.now().isoformat(), "production",
            datetime.now().isoformat(), {"precision": 0.95, "recall": 0.75},
            True, {"data":"data2"}
        )
        trained_model_id = session.create_trained_model(test_trained_model)
        returned_trained_model = session.get_trained_model(trained_model_id)
        self.assertEqual(test_trained_model.model_object, returned_trained_model.model_object)
        self.assertEqual(test_trained_model.backtest_timestamp, returned_trained_model.backtest_timestamp)