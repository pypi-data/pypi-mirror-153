"""
Utils for data management.
"""
import json
from collections import OrderedDict

from pymetadata.log import get_logger


logger = get_logger(__name__)


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def recursive_iter(obj, keys=()):
    """Creates dictionary with key:object from nested JSON data structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from recursive_iter(v, keys + (k,))
    elif any(isinstance(obj, t) for t in (list, tuple)):
        for idx, item in enumerate(obj):
            yield from recursive_iter(item, keys + (idx,))

        if len(obj) == 0:
            yield keys, None

    else:
        yield keys, obj


def set_keys(d, value, *keys):
    """Changes keys in nested dictionary."""
    for key in keys[:-1]:
        d = d[key]
    d[keys[-1]] = value


def read_json(path) -> OrderedDict:
    """Reads json.

    :param path: returns OrderedDict of JSON content, None if parsing is failing
    :return:
    """
    with open(path) as f:
        try:
            json_data = json.loads(
                f.read(),
                object_pairs_hook=ordered_dict_no_duplicates,
            )
        except json.decoder.JSONDecodeError as err:
            logger.error(f"{err}\nin {path}")
            return None
        except ValueError as err:
            logger.error(f"{err}\nin {path}")
            return None

    return json_data


def ordered_dict_no_duplicates(ordered_pairs) -> OrderedDict:
    """Reject duplicate keys and keep order"""
    d = OrderedDict()
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError("duplicate key: %r" % (k,))
        else:
            d[k] = v
    return d
