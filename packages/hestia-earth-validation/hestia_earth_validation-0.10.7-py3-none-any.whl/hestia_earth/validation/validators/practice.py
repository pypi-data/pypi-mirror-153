from hestia_earth.schema import SiteSiteType, TermTermType
from hestia_earth.utils.model import filter_list_term_type, find_term_match
from hestia_earth.utils.tools import flatten, list_sum, non_empty_list
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name

from hestia_earth.validation.utils import _filter_list, _filter_list_errors


def validate_longFallowPeriod(practices: list):
    longFallowPeriod = find_term_match(practices, 'longFallowPeriod', None)
    longFallowPeriod_index = practices.index(longFallowPeriod) if longFallowPeriod else 0
    value = list_sum(longFallowPeriod.get('value', [0])) if longFallowPeriod else 0
    rotationDuration = list_sum(find_term_match(practices, 'rotationDuration').get('value', 0))
    return value == 0 or ((rotationDuration - value) / value) < 5 or {
        'level': 'error',
        'dataPath': f".practices[{longFallowPeriod_index}].value",
        'message': 'longFallowPeriod must be lower than 5 years'
    }


def validate_cropResidueManagement(practices: list):
    practices = _filter_list(practices, 'term.termType', TermTermType.CROPRESIDUEMANAGEMENT.value)
    sum = list_sum(flatten([p.get('value', []) for p in practices]))
    return sum <= 100.5 or {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'value should sum to 100 or less across crop residue management practices',
        'params': {
            'sum': sum
        }
    }


def validate_excretaManagement(node: dict, practices: list):
    has_input = len(_filter_list(node.get('inputs', []), 'term.termType', TermTermType.EXCRETA.value)) > 0
    has_practice = len(_filter_list(practices, 'term.termType', TermTermType.EXCRETAMANAGEMENT.value)) > 0
    return not has_practice or has_input or {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'an excreta input is required when using an excretaManagement practice'
    }


NO_TILLAGE_ID = 'noTillage'


def _practice_is_tillage(practice: dict):
    term_id = practice.get('term', {}).get('@id')
    term_type = practice.get('term', {}).get('termType')
    return True if term_type == TermTermType.OPERATION.value and get_table_value(
        download_lookup('operation.csv'), 'termid', term_id, column_name('isTillage')) else False


def validate_no_tillage(practices: list):
    no_tillage = find_term_match(practices, NO_TILLAGE_ID, None)
    no_value = list_sum(no_tillage.get('value', [100]), 100) if no_tillage else 0
    return _filter_list_errors([{
        'level': 'error',
        'dataPath': f".practices[{index}]",
        'message': f"is not allowed in combination with {NO_TILLAGE_ID}"
    } for index, p in enumerate(practices) if _practice_is_tillage(p)] if no_value == 100 else [])


_TILLAGE_SITE_TYPES = [
    SiteSiteType.CROPLAND.value
]


def _unique_practice(practice: dict):
    term_id = practice.get('term', {}).get('@id')
    term_type = practice.get('term', {}).get('termType')
    return True if term_type == TermTermType.TILLAGE.value and get_table_value(
        download_lookup('tillage.csv'), 'termid', term_id, column_name('unique')) else False


def validate_tillage_site_type(practices: list, site: dict):
    has_tillage = len(filter_list_term_type(practices, TermTermType.TILLAGE)) > 0
    site_type = site.get('siteType')
    return site_type not in _TILLAGE_SITE_TYPES or has_tillage or {
        'level': 'warning',
        'dataPath': '.practices',
        'message': 'should contain a tillage practice'
    }


def _validate_tillage_with_values(practices: list):
    sum_values = sum(map(lambda p: list_sum(p.get('value', [])), practices))
    return 99.5 < sum_values < 100.5 or {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'sum not equal to 100% for tillage practices'
    }


def _validate_tillage_no_values(practices: list):
    return len(practices) <= 1 or {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'can only have 1 tillage practice without a value',
        'params': {
            'current': non_empty_list(map(lambda p: p.get('term', {}), practices))
        }
    }


def validate_tillage_values(practices: list):
    practices = list(filter(_unique_practice, practices))
    with_value = list(filter(lambda p: len(p.get('value', [])) > 0, practices))
    no_value = list(filter(lambda p: len(p.get('value', [])) == 0, practices))
    return {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'must set value for every tillage practice'
    } if (len(no_value) > 0 and len(with_value) > 0) else (
        _validate_tillage_with_values(practices) if len(with_value) > 0 else _validate_tillage_no_values(practices)
    )
