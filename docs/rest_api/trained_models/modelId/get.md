# Get Trained Model by Id
Access a single trained model.

**URL** : `/v1/trained_models/:modelId`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Data constraints**: No payload expected.

## Success Response

**Condition** : If the item was found

**Code** : `200 OK`

**Content example**

```json
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
	"training_data_start" : "2023-03-15T21:00:34.140508",
	"training_data_end" : "2023-03-18T21:00:07.274173",
	"train_timestamp" : "2023-03-18T21:00:07.274173",
	"model_object" : "abcdefabcdef...",
	"deployment_stage" : "testing"
}
```

## Error Response

**Condition** : If no trained model with that id was found

**Code** : `404 Not Found`