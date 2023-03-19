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
	"training_data_start" : "ISO-8601 formatted string",
	"training_data_end" : "ISO-8601 formatted string",
	"train_timestamp" : "ISO-8601 formatted string",
	"model_object" : "string"
	"deployment_stage" : "string"
}
```

**Data examples**:

```json
{
	"project_id" : 1,
	"parameter_set_id" : 1,
	"training_data_start" : "2023-03-15T21:00:34.140508",
	"training_data_end" : "2023-03-18T21:00:07.274173",
	"train_timestamp" : "2023-03-18T21:00:07.274173",
	"model_object" : "abcdefabcdef..."
	"deployment_stage" : "testing"
}
```

## Success Response

**Condition** : Trained model created successfully.

**Code** : `201 CREATED`

**Content example**

```json
{
    "model\_id": 123
}
```

## Error Responses

**Condition** : One of the required fields is missing or has the wrong type.

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "error": "The model\_object field is required."
}
```
