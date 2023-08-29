# ringling-cli
Command-line interface for the Ringling model management service

## Using ringling-cli
The CLI is used by running commands in the following format:

ringling-cli [host] [object-type] [action] [params]

Where:  
[host] is the url of the management process. Generally, it is ok to leave this as "localhost".

[object-type] is the type of object you wish to interface with, and is one of: ["project", "param-set", "deploy-status", "model-test-results"]

[action] is the action you wish to perform. This may vary from object type to object type (see below), but is generally one of: ["get", "create", "modify", "list"]

[params] represents command specific parameters. See below for more detail.  
--id to specify id  
--name or -N to specify the name  
--active or -A to specify set activity

## Interfacing with projects
The following commands can be used to create, list, and get projects.


#### Create
Input:  

```
ringling-cli localhost project create -N name_here
```

Output:

```
Project name_here created successfully  
Project ID: 4
```

#### List
Input:

```
ringling-cli localhost project list
```

Output:

```  
{'projects': [{'project_id': 1, 'project_name': 'test'},  
              {'project_id': 2, 'project_name': 'test2'}]}  
```

#### Get
Input:  

```
ringling-cli localhost project get --id 1
```

Output:  

```
{'project_id': 1, 'project_name': 'test'}
```

## Interfacing with Parameter Sets
The following commands can be used to create, list, modify, and get parameter sets.

#### Create
Input:  
```
ringling-cli localhost param-set create --id 2 --params "C:\Users\path\to\file.json" --active False
```

Output:
```
Parameter Set created successfully with ID 3
```

#### List
Input:  
```
ringling-cli localhost param-set list
```

Output:

```  
{'parameter_sets': [{'is_active': True,
                     'parameter_set_id': 1,
                     'project_id': 5,
                     'training_parameters': {'param1': 1, 'param2': '2'}},
                    {'is_active': False,
                     'parameter_set_id': 2,
                     'project_id': 5,
                     'training_parameters': {'param1': 1, 'param2': '3'}}]}
```

#### Get
Input:  

```
ringling-cli localhost param-set get --id 1
```

Output:  

```
{'is_active': True,
 'parameter_set_id': 1,
 'project_id': 5,
 'training_parameters': {'param1': 1, 'param2': '2'}}
```

#### Modify
Input:  

```
ringling-cli localhost param-set modify --id 5 --set-status True
```

Output:  

```
Parameter Set 5 active status changed to True
```

## Interfacing with Trained Models
The following commands can be used to create, list, modify, and get trained models.

#### Create
Input:

```
ringling-cli localhost trained-model create --project-id 2 --param-set-id 3
--train-data-start 2023-07-12T12:05:08.060499 --train-data-end 2023-07-14T12:25:08.080499
--timestamp 2023-07-17T12:05:08.060499 --model-file "C:\Users\path\to\file.pickle"
--deployment-stage testing
```

Output:
```
Trained model created with ID 11
```

#### List
Input:

```
ringling-cli localhost trained-model list
```

Output:

```
{'trained_models': [{'deployment_stage': 'testing',
                     'model_id': 1,
                     'model_object': '8004950b000000000000008f94284b014b034b05902e',
                     'parameter_set_id': 1,
                     'project_id': 5,
                     'train_timestamp': '2023-07-17T17:24:30.248546',
                     'training_data_from': '2023-07-14T17:24:30.248532',
                     'training_data_until': '2023-07-17T17:24:30.248539'},
                    {'deployment_stage': 'testing',
                     'model_id': 2,
                     'model_object': '80049513000000000000007d94288c03796573944b018c026e6f9489752e',
                     'parameter_set_id': 49,
                     'project_id': 5,
                     'train_timestamp': '2023-07-17T17:24:30.260156',
                     'training_data_from': '2023-07-14T17:24:30.260145',
                     'training_data_until': '2023-07-17T17:24:30.260151'}]}
```

#### Get
Input:

```
ringling-cli localhost trained-model get --id 9
```

Output:

```
{'deployment_stage': 'testing',
 'model_id': 9,
 'model_object': '80049513000000000000007d94288c03796573944b018c026e6f9489752e',
 'parameter_set_id': 3,
 'project_id': 2,
 'train_timestamp': '2023-07-17T12:05:08.060499',
 'training_data_from': '2023-07-12T12:05:08.060499',
 'training_data_until': '2023-07-14T12:25:08.080499'}
 ```

 #### Modify

 Input:

 ```
 localhost trained-model modify --id 1 --set-deployment-stage testing
 ```

 Output:

```
Trained Model 1 deployment status changed to testing
```

## Interfacing with Model Tests
The following commands can be used to create, list, and get trained models.

#### Create
Input:

```
ringling-cli localhost model-test create --project-id 2 --param-set-id 3
--model-id 4 --timestamp 2023-07-25T12:05:08.060499
--metrics-file "C:\Users\path\to\file.pickle" --test-passed True
```

Output:

```
Model Test created with ID 5
```

#### List
Input:

```
ringling-cli localhost model-test list
```

Output:

```
{'model_tests': [{'model_id': 2,
                  'parameter_set_id': 1,
                  'passed_testing': True,
                  'project_id': 5,
                  'test_id': 1,
                  'test_metrics': {'precision': 0.2, 'recall': 0.8},
                  'test_timestamp': '2023-07-25T20:18:34.913717'},
                 {'model_id': 2,
                  'parameter_set_id': 1,
                  'passed_testing': True,
                  'project_id': 5,
                  'test_id': 2,
                  'test_metrics': {'precision': 0.2, 'recall': 0.8},
                  'test_timestamp': '2023-07-25T20:18:34.932949'}]}
```
#### Get
Input:

```
ringling-cli localhost model-test get --id 5
```

Output:

```
{'model_id': 53,
 'parameter_set_id': 1,
 'passed_testing': True,
 'project_id': 5,
 'test_id': 5,
 'test_metrics': {'precision': 0.2, 'recall': 0.8},
 'test_timestamp': '2023-07-25T20:18:34.965780'}
```
