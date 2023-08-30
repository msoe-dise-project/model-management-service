# Ringling

Ringling is a model management service responsible for tracking:

1. Model training parameters
1. Trained models
1. Model evaluation results

## Overview
Ringling is split into client and server parts.

The server folder contains everything necessary to run the Ringling service.

The client folder contains a library to interact with Ringling and a command line interface built on top of the library.

It is recommended to first set up the server, and then the client.

## Documentation
* [Server README](server/README.md)
* [Client README](client/README.md)


* [Server Tutorial](server/docs/tutorial/ringling_tutorial.md)
* [Server Database Schema](server/docs/database_schema.md)
* [Server REST API](server/docs/rest_api/README.md)


## License

Unless otherwise noted, the source files are distributed
under the Apache Version 2.0 license found in the LICENSE file.	
