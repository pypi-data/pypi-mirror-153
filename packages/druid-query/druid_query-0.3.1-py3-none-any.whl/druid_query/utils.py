from typing import Union

from .components.intervals import Interval


def camelCase(s: str):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def druid_serealize(obj) -> Union[dict, str]:
    if isinstance(obj, Interval):
        return obj.start + '/' + obj.end
    out_dict = {}
    for i in dir(obj):
        if i.startswith('__') or callable(getattr(obj, i)):
            continue
        attr = getattr(obj, i)
        if attr is not None:
            key = camelCase(i)
            out_dict[key] = attr
    return out_dict
