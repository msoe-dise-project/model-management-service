# Create Trained Model
Creates a parameter set and assigns a unique id.

**URL** : `/v1/trained_models`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : Expects a JSON payload with the following fields.  Valid values for the deployment stage are "testing", "production", and "retired".

```json
{
	"project_id" : "integer",
	"parameter_set_id" : "integer",
	"backtest_metrics" : "object",
	"passed_backtesting" : "boolean",
  	"backtest_timestamp" : "ISO-8601 formatted string",
	"training_data_start" : "ISO-8601 formatted string",
	"training_data_end" : "ISO-8601 formatted string",
	"train_timestamp" : "ISO-8601 formatted string",
	"model_object" : "string",
	"deployment_stage" : "string"
}
```

**Data examples**:

```json
{
	"project_id" : 1,
	"parameter_set_id" : 1,
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

## Success Response

**Condition** : Trained model created successfully.

**Code** : `201 CREATED`

**Content example**

```json
{
    "model_id": 123
}
```

## Error Responses

**Condition** : One of the required fields is missing or has the wrong type.

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "error": "The model_object field is required."
}
```
