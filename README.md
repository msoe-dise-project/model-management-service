# Ringling

Ringling is a model management service responsible for tracking:

1. Model training parameters
1. Trained models
1. Model evaluation results

## Running the Service
The service can be run with Docker Compose like so:

```bash
$ docker compose build --no-cache
$ docker compose up -d
[+] Building 0.0s (0/0)
[+] Running 4/4
 ✔ Network model-management-service_default  Created                                                             0.1s
 ✔ Container postgres                        Healthy                                                             6.7s
 ✔ Container database-setup                  Exited                                                              6.6s
 ✔ Container model-management-service        Started                                                             6.9s
```

You can then check the status of the containers like so:

```bash
$ docker ps
CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS                    PORTS                                       NAMES
6426963f1945   model-management-service   "/bin/sh -c 'flask r…"   31 seconds ago   Up 24 seconds (healthy)   0.0.0.0:8888->8888/tcp, :::8888->8888/tcp   model-management-service
44669dd8b3a3   postgres:bullseye          "docker-entrypoint.s…"   32 seconds ago   Up 30 seconds (healthy)   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgres
```

Both containers should have a status of "healthy".  If you see "health: starting", wait a minute and query the status again.

Once the service is running, you can run the tests and check their output like so:

```bash
$ docker compose up -d model-management-service-tests
$ docker logs model-management-service-tests
.............................
----------------------------------------------------------------------
Ran 29 tests in 0.380s

OK
```

## Documentation

* [Tutorial](docs/tutorial/ringling_tutorial.md)
* [Database Schema](docs/database_schema.md)
* [REST API](docs/rest_api/README.md)

## License

Unless otherwise noted, the source files are distributed
under the Apache Version 2.0 license found in the LICENSE file.	
