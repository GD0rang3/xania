import hjson
import json
import re

__all__ = ["load", "loads", "dump", "dumps"]

def _normalize_key(key):
    key = key.strip()
    key = re.sub(r"\s+", "", key)
    key = re.sub(r"\.{2,}", ".", key)
    return key

def _set_nested_value(data, keys, value):
    current = data
    for i, key in enumerate(keys):
        is_last = (i == len(keys) - 1)
        is_index = key.isdigit()

        if is_index:
            index = int(key) - 1  # PHJ is 1-based index

            if isinstance(current, dict):
                # convert current into list holder if needed
                if "__list__" not in current:
                    current["__list__"] = []
                current = current["__list__"]

            while len(current) <= index:
                current.append(None)

            if is_last:
                current[index] = value
            else:
                if current[index] is None or not isinstance(current[index], dict):
                    current[index] = {}
                current = current[index]

        else:
            if "__list__" in current:
                raise TypeError("Cannot mix list and dict in the same structure")

            if is_last:
                current[key] = value
            else:
                if key not in current or not isinstance(current[key], (dict, list)):
                    current[key] = {}
                current = current[key]

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
