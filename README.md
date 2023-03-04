# Model Management Service

The model management service is responsible for two things:

1. Tracking model training parameters
1. Tracking trained models

## REST API

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

POST /models

	Create a trained_model

GET /models

	List ids of active models. Filter status by active, tested, passed_testing, etc.
	Get models for a particular parameter set.

GET /models/{modelId}

	Get a model by Id

POST /models/{modelId}/test_results

	Create testing results, timestamp, and passed / failed

PUT /models/{modelId}/active_interval

	Set start date or end date.  If dates already set, then not allowed to change.


	
