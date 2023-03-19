# Create Project
Creates a project and assigns a unique id.

**URL** : `/v1/projects`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : Expects a JSON payload with a single field ("project_name") with a string value.

```json
{
		"project_name" : "string"
}
```

**Data examples**:

```json
{
	"project_name" : "Fraudulant Transaction Detector"
}
```

## Success Response

**Condition** : Project created successfully.

**Code** : `201 CREATED`

**Content example**

```json
{
    "project_id": 123
}
```

## Error Responses

**Condition** : If the project\_name field is missing.

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "error": "The project_name field is required."
}
```