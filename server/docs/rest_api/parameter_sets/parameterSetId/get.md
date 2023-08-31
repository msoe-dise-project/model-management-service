# Get Parameter Set by Id
Access a single parameter set

**URL** : `/v1/parameter_sets/:parameterSetId`

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
	"training_parameters" : {
		"model" : { "model_type" : "RandomForestClassifier", "n_estimators" : 100 },
		"scaler" : { "type" : "StandardScaler", "with_mean" : true }
	},
	"is_active" : false
}
```

## Error Response

**Condition** : If no parameter set with that id was found

**Code** : `404 Not Found`