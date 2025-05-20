import hjson
import json
import re

__all__ = ["load", "loads", "dump", "dumps"]


def _normalize_key(key):
    key = key.strip()
    key = re.sub(r"\s+", "", key)
    key = re.sub(r"\.{2,}", ".", key)
    return key


def _ensure_list(container, key):
    if "__list__" not in container:
        container["__list__"] = []
    return container["__list__"]


def _ensure_dict(container, key):
    if key not in container or not isinstance(container[key], dict):
        container[key] = {}
    return container[key]


def _assign_list_value(container, keys, value):
    index = int(keys[0]) - 1  # PHJ is 1-indexed
    while len(container) <= index:
        container.append(None)

    if len(keys) == 1:
        container[index] = value
    else:
        if container[index] is None or not isinstance(container[index], dict):
            container[index] = {}
        _set_nested_value(container[index], keys[1:], value)


def _set_nested_value(data, keys, value):
    current = data

    for i, key in enumerate(keys):
        is_last = (i == len(keys) - 1)
        is_index = key.isdigit()

        if is_index:
            index = int(key) - 1

            if isinstance(current, dict):
                current = _ensure_list(current, key)

            if is_last:
                while len(current) <= index:
                    current.append(None)
                current[index] = value
            else:
                while len(current) <= index:
                    current.append(None)
                if current[index] is None:
                    current[index] = {}
                current = current[index]
        else:
            if "__list__" in current:
                raise TypeError("Cannot mix list and dict in the same structure")

            if is_last:
                current[key] = value
            else:
                current = _ensure_dict(current, key)


def _parse_phj(flat_data):
    result = {}
    for raw_key, value in flat_data.items():
        key = _normalize_key(raw_key)
        parts = key.split(".")
        _set_nested_value(result, parts, value)
    return result


def _finalize(data):
    if isinstance(data, dict):
        if "__list__" in data:
            return [_finalize(i) for i in data["__list__"]]
        return {k: _finalize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_finalize(i) for i in data]
    return data


def load(fp):
    raw = hjson.load(fp)
    parsed = _parse_phj(raw)
    return _finalize(parsed)


def loads(s):
    raw = hjson.loads(s)
    parsed = _parse_phj(raw)
    return _finalize(parsed)


def dump(obj, fp, **kwargs):
    return json.dump(obj, fp, indent=2, ensure_ascii=False, **kwargs)


def dumps(obj, **kwargs):
    return json.dumps(obj, indent=2, ensure_ascii=False, **kwargs)
