# Change Parameter Set Active Status
Change active status of a parameter set.

**URL** : `/v1/parameter_sets/:parameterSetId`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Data constraints**: Expects a JSON object with a single field:

```json
{
	"is_active" : "boolean"
}
```

**Data examples**:

```json
{
	"is_active" : True
}
```

## Success Response

**Condition** : If the parameter set was found and the active status was changed.

**Code** : `200 OK`

**Content example**

```json
{
		"parameter_set_id" : 1,
		"is_active" : True
}
```

## Error Response

**Condition** : If no parameter set was found with that id

**Code** : `404 Not Found`

## Error Response

**Condition** : If the active_status field was missing

**Code** : `400 Bad Request`