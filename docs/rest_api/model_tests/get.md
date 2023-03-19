# List All Model Tests
Lists all model tests.

**URL** : `/v1/model_tests`

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
    "model_tests_": [
	 	{
			"project_id" : 1,
			"parameter_set_id" : 1,
			"model_id" : 1,
			"test_id" : 1,
			"test_timestamp" : "2023-03-18T21:00:07.274173",
			"test_metrics" : { "precision" : 0.97, "recall" : 0.95 },
			"passed_testing" : True
		},
		{
			"project_id" : 1,
			"parameter_set_id" : 1,
			"model_id" : 1,
			"test_id" : 2,
			"test_timestamp" : "2023-03-18T21:00:07.274173",
			"test_metrics" : { "precision" : 0.65, "recall" : 0.36 },
			"passed_testing" : False
		},
		{
			"project_id" : 1,
			"parameter_set_id" : 1,
			"model_id" : 1,
			"test_id" : 3,
			"test_timestamp" : "2023-03-18T21:00:07.274173",
			"test_metrics" : { "precision" : 0.84, "recall" : 0.97 },
			"passed_testing" : True
		}
	 ]
}
```
