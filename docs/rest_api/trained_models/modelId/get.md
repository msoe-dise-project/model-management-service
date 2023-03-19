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
		"training_data_start" : "2023-03-15T21:00:34.140508",
		"training_data_end" : "2023-03-18T21:00:07.274173",
		"train_timestamp" : "2023-03-18T21:00:07.274173",
		"model_object" : "abcdefabcdef..."
		"deployment_stage" : "testing"
}
```

## Error Response

**Condition** : If no trained model with that id was found

**Code** : `404 Not Found`