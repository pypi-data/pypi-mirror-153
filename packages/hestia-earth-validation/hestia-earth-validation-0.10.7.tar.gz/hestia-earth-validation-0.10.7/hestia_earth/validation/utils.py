import importlib
import json
from typing import List
from functools import reduce
from datetime import datetime
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.tools import list_average, safe_parse_date


def _next_error(values: list): return next((x for x in values if x is not True), True)


def _filter_list_errors(values: list, return_single=True):
    values = list(filter(lambda x: x is not True, values))
    return True if return_single and len(values) == 0 else (values[0] if return_single and len(values) == 1 else values)


def _list_except_item(values: list, item):
    try:
        idx = values.index(item)
        return values[:idx] + values[idx+1:]
    except ValueError:
        return values


def update_error_path(error: dict, key: str, index=None):
    path = f".{key}[{index}]{error.get('dataPath')}" if index is not None else f".{key}{error.get('dataPath')}"
    return {**error, **{'dataPath': path}}


def _safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def _hash_dict(value: dict): return json.dumps(value, sort_keys=True)


def _is_same_dict(a: dict, b: dict): return _hash_dict(a) == _hash_dict(b)


def _dict_without_key(a: dict, key: str):
    no_key = a.copy()
    if key in no_key:
        no_key.pop(key)
    return no_key


def _group_nodes(nodes: List[dict]):
    def group(groups: dict, node: dict):
        type = node.get('type')
        id = node.get('id')
        if type and id:
            groups[type] = groups.get(type, {})
            groups[type][id] = node
        return groups

    return reduce(group, nodes, {})


def _hash_nodes(nodes: List[dict]):
    def group(groups: dict, node: dict):
        type = node.get('type')
        id = node.get('id')
        if type and id:
            # store the hash of the node without the `id` for uniqueness check
            key = _hash_dict(_dict_without_key(node, 'id'))
            groups[key] = groups.get(key, []) + [node]
        return groups

    return reduce(group, nodes, {})


def _get_by_key(x, y):
    return x if x is None else (
        x.get(y) if isinstance(x, dict) else list(map(lambda v: _get_dict_key(v, y), x))
    )


def _get_dict_key(value: dict, key: str): return reduce(lambda x, y: _get_by_key(x, y), key.split('.'), value)


def _value_range_error(value: int, minimum: int, maximum: int):
    return 'minimum' if minimum is not None and value < minimum else \
        'maximum' if maximum is not None and value > maximum else False


def _list_sum(values: list, prop: str): return sum(map(lambda v: _safe_cast(v.get(prop, 0), float, 0.0), values))


def _list_sum_terms(values: list, term_ids=[]):
    return sum([_value_average(node) for node in values if node.get('term', {}).get('@id') in term_ids])


def _filter_list(values: list, key: str, value): return list(filter(lambda v: _get_dict_key(v, key) == value, values))


def _compare_values(x, y):
    return next((True for item in x if item in y), False) if isinstance(x, list) and isinstance(y, list) else x == y


def _same_properties(value: dict, props: List[str]):
    def identical(test: dict):
        same_values = list(filter(lambda x: _compare_values(_get_dict_key(value, x), _get_dict_key(test, x)), props))
        return test if len(same_values) == len(props) else None
    return identical


def _value_average(node: dict, default=0):
    try:
        value = node.get('value')
        is_number = value is not None and (isinstance(value, float) or isinstance(value, int))
        return value if is_number else list_average(value, default)
    except Exception:
        return default


def _find_linked_node(node_map: dict, node: dict):
    return node_map.get(node.get('type'), {}).get(node.get('id')) or (
        download_hestia(node.get('@id'), node.get('@type')) if node.get('@id') and node.get('@type') else node
    )


def _is_before_today(date: str): return safe_parse_date(date).date() <= datetime.now().date()


def _node_year(node: dict):
    date = node.get('endDate', node.get('startDate'))
    date = safe_parse_date(date) if date else None
    return date.year if date else None


def _import_model(name: str):
    return importlib.import_module(f"hestia_earth.models.{name}").run


def run_model(model: str, term_id: str, data: dict):
    """
    Run a Hestia model from the engine models library.

    Parameters
    ----------
    model : str
        The name of the model to run.
    term_id : str
        The term to run the model on.
    data : dict
        The data used to run the model.

    Returns
    -------
    Any
        The result of the model, which can be a single `dict` or a list of `dict`s.
    """
    return _import_model(model)(term_id, data)


def run_model_from_node(node: dict, data: dict):
    """
    Run a Hestia model from the engine models library.
    To use this function, you need to use a Blank Node that contains a `methodModel` and a `term`,
    otherwise you need to use the `run_model` method.

    Parameters
    ----------
    node : dict
        The Blank Node containing a `methodModel` and a `Term`.
    data : dict
        The data used to run the model.

    Returns
    -------
    Any
        The result of the model, which can be a single `dict` or a list of `dict`s.
    """
    methodModel = node.get('methodModel', {}).get('@id')
    term_id = node.get('term', {}).get('@id')
    return run_model(methodModel, term_id, data)
