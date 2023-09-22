# Create Parameter Set
Creates a parameter set and assigns a unique id.

**URL** : `/v1/parameter_sets`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : Expects a JSON payload with a single field ("project_name") with a string value.

```json
{
	"parameter_set_id" : "integer",
	"training_parameters" : "object",
	"is_active" : "boolean",
  	"metadata": "object"
}
```

**Data examples**:

```json
{
	"parameter_set_id" : 1,
	"training_parameters" : {
		"model" : { "model_type" : "RandomForestClassifier", "n_estimators" : 100 },
		"scaler" : { "type" : "StandardScaler", "with_mean" : true }
	},
	"is_active" : false
}
```

## Success Response

**Condition** : Parameter set created successfully.

**Code** : `201 CREATED`

**Content example**

```json
{
    "parameter_set_id": 123
}
```

## Error Responses

**Condition** : One of the required fields is missing or has the wrong type.

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "error": "The training_parameters field is required."
}
```