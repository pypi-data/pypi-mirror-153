from ctypes import Union
import json
import os
from flatten_json import flatten
from typing import IO, Optional, Union, Dict, List
from pydantic import BaseModel


class DotJson:
    def __init__(
        self,
        json_path: Union[str, None],
        stream: Optional[IO[str]],
        json_paths_list: Union[List[str], None],
    ):
        if json_path is None and stream is None and json_paths_list is None:
            self.json_path = find_json_path()
            self.stream = None
            self.json_paths_list = None
        else:
            self.json_path = json_path
            self.stream = stream
            self.json_paths_list = json_paths_list

    def merge_dicts(self) -> Dict:
        merged_dict = {}
        for json_path in self.json_paths_list:
            json_dict = json.load(open(json_path))
            merged_dict.update(json_dict)
        return merged_dict

    def to_dict(self) -> Dict:
        if self.stream is not None:
            json_dict = json.load(self.stream)
        elif self.json_path is not None:
            json_dict = json.load(open(self.json_path))
        elif self.json_paths_list is not None:
            json_dict = self.merge_dicts()
        return json_dict

    def to_flattened_json_dict(self) -> Dict:
        json_dict = self.to_dict()
        flattened_json_dict = flatten(json_dict, "__")
        return flattened_json_dict

    def to_envvars(self) -> None:
        flattened_json_dict = self.to_flattened_json_dict().items()
        for k, v in flattened_json_dict:
            os.environ[str(k)] = str(v)

    def to_model(self, pydantic_model: BaseModel) -> BaseModel:
        json_dict = self.to_dict()
        data_model = pydantic_model.parse_obj(json_dict)
        return data_model


def find_json_path() -> str:
    filename = "settings.json"
    current_path = os.getcwd()
    for path, directories, files in os.walk(current_path):
        checkfile = os.path.join(current_path, filename)
        for file in files:
            currentfile = os.path.join(path, file)
            if checkfile == currentfile:
                return checkfile


def load_dotjson(
    json_path: Union[str, None] = None,
    stream: Optional[IO[str]] = None,
    json_paths_list: Union[List[str], None] = None,
) -> None:
    dotjson = DotJson(
        json_path=json_path, stream=stream, json_paths_list=json_paths_list
    )
    dotjson.to_envvars()


def dict_dotjson(
    json_path: Union[str, None] = None,
    stream: Optional[IO[str]] = None,
    json_paths_list: Union[List[str], None] = None,
) -> Dict:
    dotjson = DotJson(
        json_path=json_path, stream=stream, json_paths_list=json_paths_list
    )
    output_dict = dotjson.to_dict()
    return output_dict


def model_dotjson(
    pydantic_model: BaseModel,
    json_path: Union[str, None] = None,
    stream: Optional[IO[str]] = None,
    json_paths_list: Union[List[str], None] = None,
) -> BaseModel:
    dotjson = DotJson(
        json_path=json_path, stream=stream, json_paths_list=json_paths_list
    )
    output_dict = dotjson.to_model(pydantic_model)
    return output_dict
