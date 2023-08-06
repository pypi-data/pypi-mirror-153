# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotjson']

package_data = \
{'': ['*']}

install_requires = \
['flatten-json>=0.1.13,<0.2.0',
 'pydantic>=1.9.1,<2.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-md-report>=0.2.0,<0.3.0',
 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'dotjson',
    'version': '0.1.2',
    'description': 'Read key-value pairs from a settings.json file and set them as environment variables, dictionary or Pydantic models',
    'long_description': '# python-dotjson\n\n## Installation\nSample usage:\n```\npip install dotjson\n```\n## Introduction\nIf you want your application to derive configuration using a json file, To help you with that, you can add python-dotjson to your application to make it load the configuration from a\xa0settings.json file when it is present (e.g. in development) while remaining configurable via the environment variables.\n\nSample usage:\n```python\nfrom dotjson import load_dotjson()\n\nload_dotjson()\n```\n## Features\n* Sets config vars to env vars\n* Support for multiple settings.json files\n* Lets you deserialize settings.json file to a Pydantic Model or Dictionary \n* Auto picks the settings.json file from root directory\n* Ability to load settings from stream\n\n## load_dotjson\nThis method lets you flatten and load the settings.json file to env vars. \n\nLoad Env Vars from default settings.json\n```python\nload_dotjson()\n```\nLoad Env Vars using json path override\n```python\nload_dotjson(json_path="settings/settings.dev.json")\n```\n\nLoad Env Vars using stream\n```python\nsettings_content = \'{"apple":1,"mango":5,"fruit":{"units":["kg","pound"]}}\'\nload_dotjson(stream=StringIO(settings_content))\n```\n\nLoad Env Vars using multiple json paths\n```python\nsettings_paths = ["settings.json", "settings.dev.json"]\nload_dotjson(json_paths_list=settings_paths)\n```\n\n\n## dict_dotjson\nThis method lets you load a dictionary using the settings.json file. \n\nLoad dictionary from default settings.json\n```python\ndict_output = dict_dotjson()\n```\nLoad dictionary using json path override\n```python\ndict_output = dict_dotjson(json_path="settings/settings.dev.json")\n```\n\nLoad dictionary using stream\n```python\nsettings_content = \'{"apple":1,"mango":5,"fruit":{"units":["kg","pound"]}}\'\ndict_output = dict_dotjson(stream=StringIO(settings_content))\n```\n\nLoad dictionary using multiple json paths\n```python\nsettings_paths = ["settings.json", "settings.dev.json"]\ndict_output = dict_dotjson(json_paths_list=settings_paths)\n```\n\n## model_dotjson\nThis method lets you load a pydantic model using the settings.json file. \n\nLoad dictionary from default settings.json\n```python\nclass fruit_model(BaseModel):\n    units: List[str]\n\nclass settings_model(BaseModel):\n    apple: int\n    mango: int\n    fruit: fruit_model\n\nmodel_output = model_dotjson(settings_model)\n```\nLoad dictionary using json path override\n```python\nclass fruit_model(BaseModel):\n    units: List[str]\n\nclass settings_model(BaseModel):\n    apple: int\n    mango: int\n    fruit: fruit_model\n\nmodel_output = model_dotjson(settings_model, json_path="settings/settings.dev.json")\n```\n\nLoad dictionary using stream\n```python\nclass fruit_model(BaseModel):\n    units: List[str]\n\nclass settings_model(BaseModel):\n    apple: int\n    mango: int\n    fruit: fruit_model\n\nsettings_content = \'{"apple":1,"mango":5,"fruit":{"units":["kg","pound"]}}\'\nmodel_output = model_dotjson(settings_model, stream=StringIO(settings_content))\n\n```\n\nLoad dictionary using multiple json paths\n```python\nclass fruit_model(BaseModel):\n    units: List[str]\n\nclass settings_model(BaseModel):\n    apple: int\n    mango: int\n    fruit: fruit_model\n\nsettings_paths = ["settings.json", "settings.dev.json"]\nmodel_output = model_dotjson(settings_model, json_paths_list=settings_paths)\n```\n## Inspired by \n* python-dotjson: https://github.com/theskumar/python-dotenv\n## References\n* poetry: https://github.com/python-poetry/poetry\n* gitversion: https://github.com/GitTools/GitVersion\n* Pydantic: https://github.com/samuelcolvin/pydantic',
    'author': 'Aakash Khanna',
    'author_email': 'aakashkh13@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aakashkhanna/python-dotjson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
