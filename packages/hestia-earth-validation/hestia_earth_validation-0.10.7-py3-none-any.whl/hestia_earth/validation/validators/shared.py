import os
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
import re
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.tools import flatten, list_sum
from hestia_earth.earth_engine.gee_utils import MAX_AREA_SIZE

from hestia_earth.validation.geojson import get_geojson_area
from hestia_earth.validation.gee import is_enabled, id_to_level, get_region_id, get_region_size, get_boundary_size
from hestia_earth.validation.utils import (
    update_error_path, _filter_list_errors, _next_error, _value_average,
    _find_linked_node, _is_before_today, run_model_from_node, run_model, _get_dict_key,
    _list_except_item, _dict_without_key, _hash_dict
)


def validate_properties_same_length(node: dict, list_key: str, prop_key: str, prop_keys: list):
    def validate(values: tuple):
        index, blank_node = values
        value_len = len(blank_node.get(prop_key, ''))
        invalid_prop_key = next((
            key for key in prop_keys if blank_node.get(key) and len(blank_node.get(key)) != value_len), None)
        return value_len == 0 or invalid_prop_key is None or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].{invalid_prop_key}",
            'message': f"must have the same length as {prop_key}"
        }

    return _filter_list_errors(flatten(map(validate, enumerate(node.get(list_key, [])))))


def validate_date_lt_today(node: dict, key: str):
    return node.get(key) is None or _is_before_today(node.get(key)) or {
        'level': 'error',
        'dataPath': f".{key}",
        'message': "must be lower than today's date"
    }


def validate_list_date_lt_today(node: dict, list_key: str, node_keys: list):
    def validate(values: tuple):
        index, value = values
        errors = list(map(lambda key: {'key': key, 'error': validate_date_lt_today(value, key)}, node_keys))
        return _filter_list_errors(
            [update_error_path(error['error'], list_key, index) for error in errors if error['error'] is not True]
        )

    return _filter_list_errors(flatten(map(validate, enumerate(node.get(list_key, [])))))


def validate_dates(node: dict):
    start = node.get('startDate')
    end = node.get('endDate')
    return start is None or end is None or (len(start) <= 7 and len(end) <= 7 and end >= start) or end > start


def validate_list_dates(node: dict, list_key: str):
    def validate(values: tuple):
        index, value = values
        return validate_dates(value) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].endDate",
            'message': 'must be greater than startDate'
        }

    return _filter_list_errors(map(validate, enumerate(node.get(list_key, []))))


def validate_list_dates_format(node: dict, list_key: str):
    return validate_properties_same_length(node, list_key, 'endDate', ['startDate'])


def validate_list_dates_length(node: dict, list_key: str):
    def validate(values: tuple):
        index, blank_node = values
        value = blank_node.get('value')
        dates = blank_node.get('dates')
        return value is None or dates is None or len(dates) == len(value) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].dates",
            'message': 'must contain as many items as values',
            'params': {
                'expected': len(value),
                'current': len(dates)
            }
        }

    return _filter_list_errors(map(validate, enumerate(node.get(list_key, []))))


def _compare_min_max(value1, value2): return value1 <= value2


def _compare_list_min_max(list1: list, list2: list):
    def compare_enum(index: int):
        valid = _compare_min_max(list1[index], list2[index])
        return True if valid is True else index

    return len(list1) != len(list2) or \
        next((x for x in list(map(compare_enum, range(len(list1)))) if x is not True), True)


def validate_list_min_max(node: dict, list_key: str):
    def validate(values: tuple):
        index, value = values
        min = value.get('min', 0)
        max = value.get('max', 0)
        skip_compare = (
            isinstance(min, list) and not isinstance(max, list)
        ) or (
            isinstance(max, list) and not isinstance(min, list)
        )
        compare_lists = isinstance(min, list) and isinstance(max, list)
        is_valid = True if skip_compare else \
            _compare_list_min_max(min, max) if compare_lists else _compare_min_max(min, max)
        return is_valid is True or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].max",
            'message': 'must be greater than min'
        }

    return _next_error(list(map(validate, enumerate(node.get(list_key, [])))))


def validate_nodes_duplicates(node: dict, node_by_hash: dict):
    node_without_id = _dict_without_key(node, 'id')
    key = _hash_dict(node_without_id)
    duplicates = _list_except_item(node_by_hash.get(key, []), node)
    return [next(
        ({
            'level': 'warning',
            'dataPath': '',
            'message': f"might be a duplicate of the {dup.get('type')} with id {dup.get('id')}"
        } for dup in duplicates),
        True
    )] if len(duplicates) > 0 else []


def validate_list_duplicate_values(node: dict, list_key: str, prop: str, value: str):
    values = node.get(list_key, [])
    duplicates = list(filter(lambda v: _get_dict_key(v, prop) == value, values))
    return len(duplicates) < 2 or {
        'level': 'error',
        'dataPath': f".{list_key}[{values.index(duplicates[1])}].{prop}",
        'message': f"must have only one entry with the same {prop} = {value}"
    }


def validate_list_term_percent(node: dict, list_key: str):
    def soft_validate(index: int, value): return 0 < value and value <= 1 and {
        'level': 'warning',
        'dataPath': f".{list_key}[{index}].value",
        'message': 'may be between 0 and 100'
    }

    def hard_validate(index: int, value): return (0 <= value and value <= 100) or {
        'level': 'error',
        'dataPath': f".{list_key}[{index}].value",
        'message': 'should be between 0 and 100 (percentage)'
    }

    def validate(values: tuple):
        index, blank_node = values
        units = blank_node.get('term', {}).get('units', '')
        value = _value_average(blank_node, None) if units == '%' else None
        return value is None or type(value) == str or soft_validate(index, value) or hard_validate(index, value)

    return _filter_list_errors(map(validate, enumerate(node.get(list_key, []))))


def validate_is_region(node: dict, region_key='region'):
    region_id = node.get(region_key, {}).get('@id', '')
    level = id_to_level(region_id)
    return level > 0 or {
        'level': 'error',
        'dataPath': f".{region_key}",
        'message': 'must not be a country'
    }


def validate_region_in_country(node: dict, region_key='region'):
    country = node.get('country', {})
    region_id = node.get(region_key, {}).get('@id', '')
    return region_id[0:8] == country.get('@id') or {
        'level': 'error',
        'dataPath': f".{region_key}",
        'message': 'must be within the country',
        'params': {
            'country': country.get('name')
        }
    }


def validate_country(node: dict):
    country_id = node.get('country', {}).get('@id', '')
    # handle additional regions used as country, like region-world
    is_region = country_id.startswith('region-')
    return is_region or bool(re.search(r'GADM-[A-Z]{3}$', country_id)) or {
        'level': 'error',
        'dataPath': '.country',
        'message': 'must be a country'
    }


def need_validate_coordinates(node: dict): return is_enabled() and 'latitude' in node and 'longitude' in node


def validate_coordinates(node: dict, region_key='region'):
    latitude = node.get('latitude')
    longitude = node.get('longitude')
    country = node.get('country', {})
    region = node.get(region_key)
    gadm_id = region.get('@id') if region else country.get('@id')
    id = get_region_id(gadm_id, latitude=latitude, longitude=longitude)
    return gadm_id == id or {
        'level': 'error',
        'dataPath': f".{region_key}" if region else '.country',
        'message': 'does not contain latitude and longitude',
        'params': {
            'gadmId': id
        }
    }


def need_validate_area(node: dict): return 'area' in node and 'boundary' in node


def validate_area(node: dict):
    try:
        area = get_geojson_area(node.get('boundary'))
        return area == round(node.get('area'), 1) or {
            'level': 'error',
            'dataPath': '.area',
            'message': f"must be equal to boundary (~{area})"
        }
    except KeyError:
        # if getting the geojson fails, the geojson format is invalid
        # and the schema validation step will detect it
        return True


def validate_area_size(node: dict):
    area = node.get('area', 0) / 100
    return area < MAX_AREA_SIZE or {
        'level': 'warning',
        'dataPath': '.area',
        'message': 'should be lower than max size',
        'params': {
            'current': area,
            'expected': MAX_AREA_SIZE
        }
    }


def need_validate_boundary_size(node: dict):
    return all([
        is_enabled(),
        not need_validate_coordinates(node),
        'boundary' in node
    ])


def validate_boundary_size(node: dict):
    boundary = node.get('boundary')
    try:
        # get_boundary_size might throw error is geometry has too many edges
        area = get_boundary_size(boundary) if boundary else 0
    except Exception:
        area = 0
    return area < MAX_AREA_SIZE or {
        'level': 'warning',
        'dataPath': '.boundary',
        'message': 'should be lower than max size',
        'params': {
            'current': area,
            'expected': MAX_AREA_SIZE
        }
    }


def need_validate_region_size(node: dict):
    return all([
        is_enabled(),
        not need_validate_coordinates(node),
        not need_validate_boundary_size(node),
        'region' in node or 'country' in node
    ])


def validate_region_size(node: dict):
    region_id = node.get('region', node.get('country', {})).get('@id')
    region = download_hestia(region_id) if region_id else {}
    try:
        # get_region_size might throw error is geometry has too many edges
        area = region.get('area', get_region_size(region_id) if region_id else None) or 0
    except Exception:
        area = 0
    return area < MAX_AREA_SIZE or {
        'level': 'warning',
        'dataPath': f".{'region' if node.get('region') else 'country'}",
        'message': 'should be lower than max size',
        'params': {
            'current': area,
            'expected': MAX_AREA_SIZE
        }
    }


N_A_VALUES = [
    '#n/a',
    '#na',
    'n/a',
    'na',
    'n.a',
    'nodata',
    'no data'
]


def validate_empty_fields(node: dict):
    keys = list(filter(lambda key: isinstance(node.get(key), str), node.keys()))

    def validate(key: str):
        return not node.get(key).lower() in N_A_VALUES or {
            'level': 'warning',
            'dataPath': f".{key}",
            'message': 'may not be empty'
        }

    return _filter_list_errors(map(validate, keys), False)


def validate_linked_source_privacy(node: dict, key: str, node_map: dict = {}):
    related_source = _find_linked_node(node_map, node.get(key, {}))
    node_privacy = node.get('dataPrivate')
    related_source_privacy = related_source.get('dataPrivate') if related_source else None
    return related_source_privacy is None or node_privacy == related_source_privacy or {
        'level': 'error',
        'dataPath': '.dataPrivate',
        'message': 'should have the same privacy as the related source',
        'params': {
            'dataPrivate': node_privacy,
            key: {
                'dataPrivate': related_source_privacy
            }
        }
    }


def validate_private_has_source(node: dict, key: str):
    node_private = node.get('dataPrivate')
    return not node_private or node.get(key) is not None or {
        'level': 'warning',
        'dataPath': '.dataPrivate',
        'message': 'should add a source',
        'params': {
            'current': key
        }
    }


def value_difference(value: float, expected_value: float):
    """
    Get the difference in percentage between a value and the expected value.

    Parameters
    ----------
    value : float
        The value to check.
    expected_value : float
        The expected value.

    Returns
    -------
    bool
        The difference in percentage between the value and the expected value.
    """
    return 0 if (isinstance(expected_value, list) and len(expected_value) == 0) or expected_value == 0 else (
        round(abs(value - expected_value) / expected_value, 4)
    )


def is_value_different(value: float, expected_value: float, delta: float = 0.05) -> bool:
    """
    Check the difference in percentage between a value and the expected value.

    Parameters
    ----------
    value : float
        The value to check.
    expected_value : float
        The value it should be close to.
    delta : float
        The accepted difference between the value and the expected one. Defaults to `5%`.

    Returns
    -------
    bool
        `True` if the value is within the percentage of the expected value, `False` otherwise.
    """
    return value_difference(value, expected_value) > delta


def _model_value_from_list(results: list, default_value: float):
    return results[0].get('value', [default_value]) if len(results) > 0 else default_value


def _model_value(result, default_value=0):
    return default_value if result is None else (
        _model_value_from_list(result, default_value) if isinstance(result, list) else (
            result.get('value', [default_value]) if isinstance(result, dict) else default_value
        )
    )


def _value_from_model(result):
    value = _model_value(result)
    try:
        # fix numpy.float64
        # TODO: find a better way to handle this
        return list_sum(value, float(value))
    except Exception:
        return list_sum(value, value)


def _parse_node_value(node: dict):
    def parse_list_value(value: list):
        return list_sum(value) if len(value) > 0 else None

    value = node.get('value')
    return None if value is None else (
        parse_list_value(value) if isinstance(value, list) else value
    )


def _validate_list_model(node: dict, list_key: str, max_delta: float = 0.05):
    def validate(values: tuple):
        index, blank_node = values
        try:
            value = _parse_node_value(blank_node)
            # skip validation if `value` is not set
            result = run_model_from_node(blank_node, node) if value is not None else None
            expected_value = _value_from_model(result) if result else 0
            delta = value_difference(value, expected_value)
            return delta < max_delta or {
                'level': 'error',
                'dataPath': f".{list_key}[{index}].value",
                'message': 'the value provided is not consistent with the model result',
                'params': {
                    'model': blank_node.get('methodModel', {}),
                    'term': blank_node.get('term', {}),
                    'current': value,
                    'expected': expected_value,
                    'delta': delta * 100,
                    'threshold': max_delta
                }
            }
        except Exception:
            return True
    return validate


def validate_list_model(node: dict, list_key: str) -> list:
    """
    Validates a list using the engine models.
    This method will go through every element of the list and run the model that matches the
    `methodModel` and `term.@id` on the element.

    Parameters
    ----------
    node : dict
        The node containing the list to run.
    list_key : str
        The property of the node containing the list to run.

    Returns
    -------
    list
        List of errors from the models or `True` if no errors.
    """
    run = os.environ.get('VALIDATE_MODELS', 'true') == 'true'
    nodes = node.get(list_key, [])
    with ThreadPoolExecutor() as executor:
        errors = list(executor.map(_validate_list_model(node, list_key), enumerate(nodes))) if run else []
    return _filter_list_errors(errors)


def _reset_dataCompleteness(node: dict):
    dataCompleteness = node.get('dataCompleteness', {})
    dataCompleteness = reduce(lambda prev, curr: {**prev, curr: False}, dataCompleteness.keys(), dataCompleteness)
    return {**node, 'dataCompleteness': dataCompleteness}


def _validate_list_model_config(node: dict, list_key: str, conf: dict):
    def validate_model(term: dict, value: float, index: int, model_conf: dict):
        node_run = _reset_dataCompleteness(node) if model_conf.get('resetDataCompleteness', False) else node
        expected_result = run_model(model_conf['model'], term.get('@id'), node_run)
        expected_value = _value_from_model(expected_result)
        delta = value_difference(value, expected_value)
        return delta < model_conf['delta'] or {
            'level': model_conf.get('level', 'error'),
            'dataPath': f".{list_key}[{index}].value",
            'message': 'the value provided is not consistent with the model result',
            'params': {
                'model': expected_result[0].get('methodModel', {}),
                'term': term,
                'current': value,
                'expected': expected_value,
                'delta': delta * 100,
                'threshold': model_conf['delta']
            }
        }

    def validate(values: tuple):
        index, blank_node = values
        value = _parse_node_value(blank_node)
        term = blank_node.get('term', {})
        term_id = blank_node.get('term', {}).get('@id')
        # get the configuration for this element
        # if it does not exist or no `value` is set, skip model
        term_conf = conf.get(term_id)
        return validate_model(term, value, index, term_conf) if term_conf and value is not None else True

    return validate


def validate_list_model_config(node: dict, list_key: str, conf: dict):
    """
    Validates a list using the engine models.
    This method uses a configuration to determine which `term` in the elements should run.
    It does not use the `methodModel` that could be found on each element.

    Parameters
    ----------
    node : dict
        The node containing the list to run.
    list_key : str
        The property of the node containing the list to run.
    conf : dict
        The configuration to decide which models to run.

    Returns
    -------
    list
        List of errors from the models or `True` if no errors.
    """
    run = os.environ.get('VALIDATE_MODELS', 'true') == 'true'
    nodes = node.get(list_key, [])
    with ThreadPoolExecutor() as executor:
        errors = list(executor.map(_validate_list_model_config(node, list_key,  conf), enumerate(nodes))) if run else []
    return _filter_list_errors(errors)
