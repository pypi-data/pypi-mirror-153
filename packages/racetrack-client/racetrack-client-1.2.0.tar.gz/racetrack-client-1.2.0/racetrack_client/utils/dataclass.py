import dataclasses
from typing import Dict, List, Type, TypeVar

import dacite
import yaml

T = TypeVar("T")


def parse_dict_dataclass(
    obj_dict: Dict, 
    clazz: Type[T], 
    cast_types: List[Type] = None,
) -> T:
    """
    Cast dict object to expected dataclass
    :param obj_dict: dict object to be transformed to dataclass
    :param clazz: dataclass type
    :param cast_types: list of class types to be casted from primitive types.
    It should contain all class types (non-primitive and non-dataclass types) 
    that needs to be converted from a string.
    An instance of a field type will be created from the input data with 
    just calling the type with the input value.
    For instance, it solves the mismatch when dataclass field expects
    the enum type, but the string value was given.
    """
    return dacite.from_dict(
        data_class=clazz, 
        data=obj_dict, 
        config=dacite.Config(check_types=True, strict=True, cast=cast_types or []),
    )


def parse_dict_dataclasses(
    obj_list: List[Dict],
    clazz: Type[T],
    cast_types: List[Type] = None,
) -> List[T]:
    """Cast list of dict objects to expected dataclass types"""
    return [parse_dict_dataclass(obj_dict, clazz, cast_types) for obj_dict in obj_list]


def parse_yaml_dataclass(
    yaml_obj: str,
    clazz: Type[T],
    cast_types: List[Type] = None,
) -> T:
    """
    Parse YAML and convert it to expected dataclass
    :param yaml_obj: YAML string
    :param clazz: dataclass type
    :param cast_types: list of class types to be casted from primitive types.
    """
    data = yaml.load(yaml_obj, Loader=yaml.FullLoader)
    return parse_dict_dataclass(data, clazz, cast_types)


def dataclass_to_yaml_str(dt) -> str:
    data_dict = dataclass_to_dict(dt)
    return yaml.dump(data_dict)


def dataclass_to_dict(dt) -> Dict:
    data_dict = dataclasses.asdict(dt)
    data_dict = _remove_none(data_dict)
    data_dict = convert_to_json_serializable(data_dict)
    return data_dict


def _remove_none(obj):
    """Remove unwanted null values"""
    if isinstance(obj, list):
        return [_remove_none(x) for x in obj if x is not None]
    elif isinstance(obj, dict):
        return {k: _remove_none(v) for k, v in obj.items() if k is not None and v is not None}
    else:
        return obj


def convert_to_json_serializable(obj):
    if isinstance(obj, list):
        return [convert_to_json_serializable(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_json_serializable(v) for k, v in obj.items()}
    elif hasattr(obj, '__to_json__'):
        return getattr(obj, '__to_json__')()
    else:
        return obj
