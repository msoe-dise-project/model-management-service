# Create a Model Test
Creates a model test and assigns a unique id.

**URL** : `/v1/model_tests`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : Expects a JSON payload:

```json
{
	"project_id" : "integer",
	"parameter_set_id" : "integer",
	"model_id" : "integer",
	"test_timestamp" : "ISO-8601 formatted timestamp",
	"test_metrics" : "object",
	"passed_testing" : "boolean"
}
```

**Data examples**:

```json
{
	"project_id" : 1,
	"parameter_set_id" : 1,
	"model_id" : 1,
	"test_timestamp" : "2023-03-18T21:00:07.274173",
	"test_metrics" : { "precision" : 0.97, "recall" : 0.95 },
	"passed_testing" : true
}
```

## Success Response

**Condition** : Model test created successfully.

**Code** : `201 CREATED`

**Content example**

```json
{
    "test_id": 123
}
```

## Error Responses

**Condition** : One of the required fields is missing or has the wrong type.

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "error": "The test_metrics field is required."
}
```