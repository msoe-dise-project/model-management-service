# REST API


## Projects
```
POST /projects
```

> Create a project

```
GET /projects
```

> List projects

```
GET /projects/{productId}
```

> Get a specific project


## Parameter Sets

```
POST /parameter_sets
```

> Create a parameter set.  Expects what?

```
GET /parameter_sets
```

> Get list of ids.  Filter by status such as active.

```
GET /parameter_sets/{setId}
```

> Get a parameter set by id

```
PATCH /parameter_sets/{setId}
```

> Update the is\_active status


## Trained Models
```
POST /trained_models
```

> Create a trained_model

```
GET /trained_models
```

> List ids of trained models. Filter status by active, tested, passed_testing, etc.
> Get models for a particular parameter set.

```
GET /trained_models/{modelId}
```

> Get a model by Id

```
PATCH /trained_models/{modelId}
```

> Set deployment stage.  Valid values are `testing`, `production`, or `retired`.

## Model Tests

```	
POST /model_tests
```

> Create model test results

```
GET /model_tests
```

> List ids of model test results.  Filter by passed vs failed tests.

```
GET /model_tests/{modelId}
```

> Get a model test results by Id

	
