# List All Projects
Lists all projects.

**URL** : `/v1/projects`

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
    "projects": [
	 	{
			"project_name" : "Fraud Detection",
			"project_id" : 1
		},
		{
			"project_name" : "Recommendation System",
			"project_id" : 2
		}
	 ]
}
```
