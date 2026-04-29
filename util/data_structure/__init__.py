from dataclasses import is_dataclass, fields


def d_class_to_dict(obj: object, d_class) -> dict:
    obj_json = {}
    if not is_dataclass(d_class): return obj_json
    for field in fields(d_class):
        key = getattr(d_class, field.name)
        obj_json[key] = getattr(obj, key)
        pass
    return obj_json


def d_class_to_obj(obj: object, d_class, data: dict):
    if not is_dataclass(d_class): return
    for field in fields(d_class):
        key = getattr(d_class, field.name)
        if key in data and data[key] is not None:
            setattr(obj, key, data[key])
        pass
    pass
