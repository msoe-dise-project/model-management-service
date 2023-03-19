# Perform Healthcheck
Checks that the application can access the database and the tables exist.

**URL** : `healthcheck`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : No payload expected.

## Success Response

**Condition** : If can connect to database and query the expected tables.

**Code** : `200 Success`

**Content example**

```json
    {
        "database" :
        {
            "healthy" : true,
            
            "connection" :
            {
                "healthy" : true
            },
            
            "tables" :
            {
                "healthy" : True,
                "successful_queries" : ["model_tests", "parameter_sets", "projects", "trained_models"]
            }    
        }
    }
```

## Error Response

**Condition** : If the application cannot connect to the database or query the expected tables.

**Code** : `500 Internal Server Error`

**Content example**

```json
    {
        "database" :
        {
            "healthy" : true,
            
            "connection" :
            {
                "healthy" : false
            },
            
            "tables" :
            {
                "healthy" : false,
                "successful_queries" : []
            }    
        }
    }
```

OR

```json
    {
        "database" :
        {
            "healthy" : true,
            
            "connection" :
            {
                "healthy" : true
            },
            
            "tables" :
            {
                "healthy" : false,
                "successful_queries" : ["model_tests", "projects"]
            }    
        }
    }
```

