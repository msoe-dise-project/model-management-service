# List All Trained Models
Lists all trained models.

**URL** : `/v1/trained_models`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : No payload expected.

## Success Response

**Condition** : If everything is okay.

**Code** : `200 Success`

**Content example**

```json
{
    "trained_models": [
	 	{
			"project_id" : 1,
			"parameter_set_id" : 1,
			"model_id" : 1, 
			"backtest_metrics" : {"accuracy": 0.850609756097561,
                                              "accuracy_std": 0.019521720236075776,
                                              "auroc": 0.8500733994974246,
                                              "auroc_std": 0.01980587001464519,
                                              "precision": 0.8377163295641556,
                                              "precision_std": 0.038996281267517356,
                                              "recall": 0.8867752114448577,
                                              "recall_std": 0.017109439332137488},
			"passed_backtesting" : true,
			"backtest_timestamp" : "2023-03-19T12:10:55.438305",
			"training_data_from" : "2023-03-15T21:00:34.140508",
			"training_data_until" : "2023-03-18T21:00:07.274173",
			"train_timestamp" : "2023-03-18T21:00:07.274173",
			"deployment_stage" : "testing",
			"model_object" : "8004950b000000000000008f94284b154b0d4b05902e"
		},
		{
			"project_id" : 1,
			"parameter_set_id" : 1,
			"model_id" : 2,
			"backtest_metrics" : {"accuracy": 0.860609756097561,
                                              "accuracy_std": 0.015521720236075776,
                                              "auroc": 0.8700733994974246,
                                              "auroc_std": 0.01680587001464519},
			"passed_backtesting" : true,
			"backtest_timestamp" : "2023-03-19T12:10:55.438305",
			"training_data_from" : "2023-03-15T21:00:34.140508",
			"training_data_until" : "2023-03-18T21:00:07.274173",
			"train_timestamp" : "2023-03-18T21:00:07.274173",
			"deployment_stage" : "production",
			"model_object" : "8004950b000000000000008f94284b154b0d4b05902e"
		},
		{
			"project_id" : 1,
			"parameter_set_id" : 1,
			"model_id" : 3,
			"backtest_metrics" : {"precision": 0.8667163295641556,
                                              "precision_std": 0.032996281267517356,
                                              "recall": 0.8977752114448577,
                                              "recall_std": 0.016109439332137488},
			"passed_backtesting" : true,
			"backtest_timestamp" : "2023-03-19T12:10:55.438305",
			"training_data_from" : "2023-03-15T21:00:34.140508",
			"training_data_until" : "2023-03-18T21:00:07.274173",
			"train_timestamp" : "2023-03-18T21:00:07.274173",
			"deployment_stage" : "retired",
			"model_object" : "8004950b000000000000008f94284b154b0d4b05902e"
		}
	 ]
}
```
