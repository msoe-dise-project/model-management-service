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
			"training_data_start" : "2023-03-15T21:00:34.140508",
			"training_data_end" : "2023-03-18T21:00:07.274173",
			"train_timestamp" : "2023-03-18T21:00:07.274173",
			"deployment_stage" : "testing"
		},
		{
			"project_id" : 1,
			"parameter_set_id" : 1,
			"model_id" : 2,
			"training_data_start" : "2023-03-15T21:00:34.140508",
			"training_data_end" : "2023-03-18T21:00:07.274173",
			"train_timestamp" : "2023-03-18T21:00:07.274173",
			"deployment_stage" : "production"
		},
		{
			"project_id" : 1,
			"parameter_set_id" : 1,
			"model_id" : 3,
			"training_data_start" : "2023-03-15T21:00:34.140508",
			"training_data_end" : "2023-03-18T21:00:07.274173",
			"train_timestamp" : "2023-03-18T21:00:07.274173",
			"deployment_stage" : "retired"
		}
	 ]
}
```
