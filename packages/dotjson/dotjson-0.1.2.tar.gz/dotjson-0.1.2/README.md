# python-dotjson

## Installation
Sample usage:
```
pip install dotjson
```
## Introduction
If you want your application to derive configuration using a json file, To help you with that, you can add python-dotjson to your application to make it load the configuration from a settings.json file when it is present (e.g. in development) while remaining configurable via the environment variables.

Sample usage:
```python
from dotjson import load_dotjson()

load_dotjson()
```
## Features
* Sets config vars to env vars
* Support for multiple settings.json files
* Lets you deserialize settings.json file to a Pydantic Model or Dictionary 
* Auto picks the settings.json file from root directory
* Ability to load settings from stream

## load_dotjson
This method lets you flatten and load the settings.json file to env vars. 

Load Env Vars from default settings.json
```python
load_dotjson()
```
Load Env Vars using json path override
```python
load_dotjson(json_path="settings/settings.dev.json")
```

Load Env Vars using stream
```python
settings_content = '{"apple":1,"mango":5,"fruit":{"units":["kg","pound"]}}'
load_dotjson(stream=StringIO(settings_content))
```

Load Env Vars using multiple json paths
```python
settings_paths = ["settings.json", "settings.dev.json"]
load_dotjson(json_paths_list=settings_paths)
```


## dict_dotjson
This method lets you load a dictionary using the settings.json file. 

Load dictionary from default settings.json
```python
dict_output = dict_dotjson()
```
Load dictionary using json path override
```python
dict_output = dict_dotjson(json_path="settings/settings.dev.json")
```

Load dictionary using stream
```python
settings_content = '{"apple":1,"mango":5,"fruit":{"units":["kg","pound"]}}'
dict_output = dict_dotjson(stream=StringIO(settings_content))
```

Load dictionary using multiple json paths
```python
settings_paths = ["settings.json", "settings.dev.json"]
dict_output = dict_dotjson(json_paths_list=settings_paths)
```

## model_dotjson
This method lets you load a pydantic model using the settings.json file. 

Load dictionary from default settings.json
```python
class fruit_model(BaseModel):
    units: List[str]

class settings_model(BaseModel):
    apple: int
    mango: int
    fruit: fruit_model

model_output = model_dotjson(settings_model)
```
Load dictionary using json path override
```python
class fruit_model(BaseModel):
    units: List[str]

class settings_model(BaseModel):
    apple: int
    mango: int
    fruit: fruit_model

model_output = model_dotjson(settings_model, json_path="settings/settings.dev.json")
```

Load dictionary using stream
```python
class fruit_model(BaseModel):
    units: List[str]

class settings_model(BaseModel):
    apple: int
    mango: int
    fruit: fruit_model

settings_content = '{"apple":1,"mango":5,"fruit":{"units":["kg","pound"]}}'
model_output = model_dotjson(settings_model, stream=StringIO(settings_content))

```

Load dictionary using multiple json paths
```python
class fruit_model(BaseModel):
    units: List[str]

class settings_model(BaseModel):
    apple: int
    mango: int
    fruit: fruit_model

settings_paths = ["settings.json", "settings.dev.json"]
model_output = model_dotjson(settings_model, json_paths_list=settings_paths)
```
## Inspired by 
* python-dotjson: https://github.com/theskumar/python-dotenv
## References
* poetry: https://github.com/python-poetry/poetry
* gitversion: https://github.com/GitTools/GitVersion
* Pydantic: https://github.com/samuelcolvin/pydantic