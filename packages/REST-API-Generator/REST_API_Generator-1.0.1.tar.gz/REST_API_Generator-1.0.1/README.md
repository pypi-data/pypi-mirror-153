# REST-API-GENERATOR
[![](https://img.shields.io/badge/pypi-v1.0.1-blue)](https://pypi.org/project/REST-API-Generator/)  
![](https://img.shields.io/badge/python-v3.6%7Cv3.7%7Cv3.8%7Cv3.9-brightgreen)

**REST-API-GENERATOR** is a python tool that helps reduce the time it takes to create dummy REST endpoints during the initial stages of your project.

## Installation
` pip install REST-API-Generator `

## Supported Frameworks
>1. Sanic

## How to use it

To use **REST-API-GENERATOR** package to create dummy REST endpoints you have to provide a `python dict` as an input. This `python dict` shall contain all the necessary information of the REST endpoints that you want to build.  

#### *Take a look at the sample input json file below*

```
{  
    "project_dir": "~/project_dir",  
    "project_name": "Test_project",
    "api_module_name" : "webapp" 
    "framework_object": "app",
    "framekwork": "sanic",  
    "host": "0.0.0.0",  
    "port": "1201",  
    "api_list": [ 
        {  
            "method_handler_name": "get_name",  
            "HTTP_method": "GET",  
            "path": "/name",  
            "response": [  
                "name1",  
                "name2"  
            ]  
        },  
        {  
            "method_handler_name": "add_name",  
            "HTTP_method": "POST",  
            "path": "/add_name",  
            "response": "new_name"  
        },  
        {  
            "method_handler_name": "update_name",  
            "HTTP_method": "PUT",  
            "path": "/update_name",  
            "response": "name3"  
        }
    ]  
}  
```
```
project_dir         : root directory path of the project (required)
project_name        : name of the project (required)
api_module_name     : name of the API module --default : 'webapp'
framework_object    : name of the framework object --default : 'app'
framekwork          : name of the framework in which the project is created (required)
host                : host address of the server (required)
port                : port address of the server (required)

api_list        : list of all the individual end points
    method_handler_name : name of a method handler of a particular end-point (required)
    HTTP_method         : HTTP method type (required)
    path                : url path (required)
    response            : sample response (required)
```


` Use the following python script to generate dummy end-points `

#### - ***Sanic framework***
```
from API_Gen import SanicGenerator
import json

if __name__ == '__main__':
    with open('input.json') as file:
        api_info = json.load(file)
    sp = SanicGenerator(api_info=api_info)
    # 1. Use create_apis() to generate a new API layer
    sp.create_apis()
    # 2. Use add_apis() to add new endpoints to exixting API layer
    sp.create_apis()
```
