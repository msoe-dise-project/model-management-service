# Get Project by Id
Access a single project

**URL** : `/v1/projects/:projectId`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Data constraints**: No payload expected.

## Success Response

**Condition** : If the item was found

**Code** : `200 OK`

**Content example**

```json
{
	"metadata": {"meta1": 1, "meta2": 2},
	"project_name" : "Fraud Detection",
	"project_id" : 1
}
```

## Error Response

**Condition** : If no project with that id was found

**Code** : `404 Not Found`

**Content example**

```json
{
    "error": "ID 5 not found"
}
```
