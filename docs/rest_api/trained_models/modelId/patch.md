# Change Trained Model Deployment Stage
Change the deployment stage of a model

**URL** : `/v1/trained_models/:modelId`

**Method** : `PATCH`

**Auth required** : NO

**Permissions required** : None

**Data constraints**: Expects a JSON object with a single field.  Valid values are "testing", "production", and "retired".

```json
{
	"deployment_stage" : "string"
}
```

**Data examples**:

```json
{
	"deployment_stage" : "testing"
}
```

## Success Response

**Condition** : If the trained model was found and the deployment stage was changed.

**Code** : `200 OK`

**Content example**

```json
{
		"model_id" : 1,
		"deployment_stage" : "testing"
}
```

## Error Response

**Condition** : If no trained model with that id was found

**Code** : `404 Not Found`

## Error Response

**Condition** : If the deployment stage is missing

**Code** : `400 Bad Request`