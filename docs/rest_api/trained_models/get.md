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
			"training_data_from" : "2023-03-15T21:00:34.140508",
			"training_data_until" : "2023-03-18T21:00:07.274173",
			"train_timestamp" : "2023-03-18T21:00:07.274173",
			"deployment_stage" : "retired",
			"model_object" : "8004950b000000000000008f94284b154b0d4b05902e"
		}
	 ]
}
```
