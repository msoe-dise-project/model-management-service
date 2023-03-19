# REST API

## Project-Related

* [Create project](projects/post.md) : `POST /v1/projects`
* [List projects](projects/get.md) : `GET /v1/projects`
* [Get project by id](projects/projectId/get.md) : `GET /v1/projects/:projectId`

## Parameter Set-Related

* [Create paramater set](parameter_sets/post.md) : `POST /v1/parameter_sets`
* [List parameter sets](parameter_sets/get.md) : `GET /v1/parameter_sets`
* [Get parameter set by id](parameter_sets/parameterSetId/get.md) : `GET /v1/parameter_sets/:parameterSetId`
* [Update activity status of a parameter set](parameter_sets/parameterSetId/patch.md) : `PATCH /v1/parameter_sets/:parameterSetId`

## Trained Model-Related

* [Create a trained model](trained_models/post.md) : `POST /v1/trained_models`
* [List trained models](trained_models/get.md) : `GET /v1/trained_models`
* [Get trained model by id](trained_models/modelId/get.md) : `GET /v1/trained_models/:modelId`
* [Update deployment stage of a trained model](trained_models/modelId/patch.md) : `PATCH /v1/trained_models/:modelId`

## Model Tests-Related

* [Create a model test](model_tests/post.md) : `POST /v1/model_tests`
* [List model tests](model_tests/get.md) : `GET /v1/model_tests`
* [Get model test by id](model_tests/testId/get.md) : `GET /v1/model_tests/:testId`

## Health Check-Related

* [Perform health check](healthcheck/get.md) : `GET /healthcheck`

The file system layout and endpoint templates follow the examples provided by [@iros](https://gist.github.com/iros/3426278) and [@jamescooke](https://github.com/jamescooke/restapidocs).
