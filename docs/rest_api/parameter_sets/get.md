# List All Parameter Ssets
Lists all parameter sets.

**URL** : `/v1/parameter_sets`

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
    "parameter_sets": [
	 	{
			"project_id" : 1,
			"parameter_set_id" : 1,
			"training_parameters" : {
				"model" : { "model_type" : "RandomForestClassifier", "n_estimators" : 100 },
				"scaler" : { "type" : "StandardScaler", "with_mean" : True }
			},
			"is_active" : False
		},
		{
			"project_id" : 1,
			"parameter_set_id" : 2,
			"training_parameters" : {
				"model" : { "model_type" : "SGDClassifier", "alpha" : 0.01, "loss" : "log_loss" },
				"scaler" : { "type" : "StandardScaler", "with_mean" : True }
			},
			"is_active" : True
		}
	 ]
}
```
