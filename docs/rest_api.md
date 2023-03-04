# REST API

```
POST /projects

	Create a project

GET /projects

	List projects

GET /projects/{productId}

	Get a specific project

PUT /projects/{projectId}

	Set start date or end date.  If dates already set, then not allowed to change.

POST /parameter_sets

	Create a parameter set.  Expects what?

GET /parameter_sets

	Get list of ids.  Filter by status such as active.

GET /parameter_sets/{setId}

	Get a parameter set by id

PUT /parameter_sets/{setId}

	Update the active start and/or active end properties

POST /trained_models

	Create a trained_model

GET /trained_models

	List ids of trained models. Filter status by active, tested, passed_testing, etc.
	Get models for a particular parameter set.

GET /trained_models/{modelId}

	Get a model by Id

PUT /trained_models/{modelId}/active_interval

	Set start date or end date.  If dates already set, then not allowed to change.
	
POST /model_tests

	Create model test results

GET /model_tests

	List ids of model test results.  Filter by passed vs failed tests.

GET /model_tests/{modelId}

	Get a model test results by Id

```
	
