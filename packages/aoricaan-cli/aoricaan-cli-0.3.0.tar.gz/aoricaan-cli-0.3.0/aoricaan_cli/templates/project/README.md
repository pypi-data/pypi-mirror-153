# {{Project name}}

***

- [Installation](#Installation)
- [Lambdas](#Lambdas)
    * [Create a simple new lambda](#)
    * [Create a new lambda with endpoint](#)
    * [Create a new lambda with endpoint and cors](#)
    * [Rename lambda](#)
    * [Rename Endpoint](#)
    * [Show all lambdas in the project](#)
    * [Show all endpoints in the project](#)
    * [delete a lambda](#)
    * [delete only the endpoint](#)
    * [Add endpoint to existent lambda](#)

- [Layers](#Layers)
    * [Install](#)
    * [Adding new layer](#)
    * [Adding modules to the new layer](#)

- [API](#API)
    * [Run in local](#)

- [Project](#)
    * [Install layers](#)
    * [Synth project for deploy](#)
    * [Init a new project](#)

***


You need add the next environment variables also you can add the .env file in the root path for the project.

* ENVIRONMENT: [Name of the environ in use.]
* DEVELOPER: [your name]
* DB_NAME: [name of the database]
* DB_USER: [user for database]
* DB_PASSWORD: [password for database]
* DB_HOST: [host for database]
* DB_PORT: [port for database]

Note: If you use a IAM connection, in password you need add a token generated

```python
import boto3

client = boto3.client("rds")
password = client.generate_db_auth_token(
    DBHostname="",
    DBUsername="",
    Port=""
)
```

## Lambdas

### Create a simple new lambd

````commandline
apm lambda new --name [lambda name]
````

### Create a new lambda with endpoint.

````commandline
apm endpoint new --name [lambda name] --endpoint [endpoint path] --verb [get|put|post|path|delete]
````

### Create a new lambda with endpoint and cors

````commandline
apm endpoint new --name [lambda name] --endpoint [endpoint path] --verb [get|put|post|path|delete] --cors
````

The commands above makes a folder in .src/lambdas/[lambda-name] with the next structure

```
Backend 
│
└───src
│   │
│   └───lambdas
│   │   │
│   │   └───[lambda-name]
│   │   │   │   __init__.py
│   │   │   │   configuration.json
│   │   │   │   lambda_function.py
│   │   │   │   test_lambda_function.py
│   │   │   │   

---------------------------------------------------------------------
__init__.py             --> Only used for mark folder like module.
configuration.json      --> Here is all configuration for the lambda.
lambda_function.py      --> Here is the code for the lambda.
test_lambda_function.py --> Here is the test for the lambda.
```

### Add endpoint to existent lambda

````commandline
apm endpoint add --lambda-name [lambda name] --endpoint [endpoint path] --verb [get|put|post|path|delete]
````

### Rename lambda

````commandline
apm lambda rename --name [actual-name] --new-name [new-name]
```` 

### Rename Endpoint

````commandline
apm lambda rename --lambda-name [lambda-name] --new-endpoint-name [new-endpoint name]
````

### Show all lambdas in the project

````commandline
apm lambda list
````

### Show all endpoints in the project

````commandline
apm endpoint list
````

### delete a lambda

````commandline
apm lambda delete --name [lambda-name]
````

### delete only the endpoint

````commandline
apm endpoint delete --name [lambda-name]
````


NOTE: All arguments for the commands 

## Layers

### Adding new layer

````commandline
apm layer new --name [lambda name]
````

1. Create a new folder in the path ./src/layers

```
Backend 
│
└───src
│   │
│   └───layers
│   │   │
│   │   └───[new_layer]
│   │   │   │   
│   │   │   └───python
│   │   │   │   │   ...

```

2.Add the cfn configuration in the [projectTemplate.json]('./projectTemplate.json) in the node **Resources**.

```
    "Layer[layerName]": {
      "Type": "AWS::Lambda::LayerVersion",
      "Properties": {
        "CompatibleRuntimes": [
          "python3.9"
        ],
        "Content": "src/layers/[layer_name]",
        "LayerName": {
          "Fn::Sub": "${Environment}-[layer_name]"
        }
      }
    }
```

### Adding modules to the new layer

1. Inside the folder of the layer to which you want to add a module, create a folder with a file \_\_init__.py.
2. Inside that folder you can put your scripts with the new functionalities of the module.

The structure of the folder should look like this:

```
Backend 
│
└───src
│   │
│   └───layers
│   │   │   
│   │   └───[new_layer]
│   │   │   │   
│   │   │   └───python
│   │   │   │   │   
│   │   │   │   └───[module-1]
│   │   │   │   │   │   __init__.py
│   │   │   │   │   │   [module1].py
│   │   │   │   │   │
│   │   │   │   └───[module-2]
│   │   │   │   │   │   __init__.py
│   │   │   │   │   │   [module2].py
│   │   │   │   │   │
│   │   │   │   │   ...
│   │   │   │   │   
│   │   │   ...
│   │   │   

```

3. Add the module reference to ./utils/install_layers.py (Module that are not referenced in this list will not be
   installed on your local machine when using the command ``python console.py --install``)

```python
import os

...

LAYERS = [
    os.path.join('src', 'layers', 'core', 'python', 'api'),
    os.path.join('src', 'layers', '[you_layer]', 'python', '[your_module]'),
    ...
]

...
```

