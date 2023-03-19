# Get Model Test by Id
Access a single model test.

**URL** : `/v1/model_tests/:modelId`

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
	"test_id" : 1,
	"test_timestamp" : "2023-03-18T21:00:07.274173",
	"test_metrics" : { "precision" : 0.97, "recall" : 0.95 },
	"passed_testing" : True
}
```

## Error Response

**Condition** : If no trained model with that id was found

**Code** : `404 Not Found`