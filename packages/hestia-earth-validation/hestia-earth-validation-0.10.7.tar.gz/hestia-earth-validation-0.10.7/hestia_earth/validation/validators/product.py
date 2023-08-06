from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.lookup import get_table_value, download_lookup
from hestia_earth.utils.tools import list_sum, flatten

from hestia_earth.validation.utils import _list_sum, _filter_list_errors


def validate_economicValueShare(products: list):
    sum = _list_sum(products, 'economicValueShare')
    return sum <= 100.5 or {
        'level': 'error',
        'dataPath': '.products',
        'message': 'economicValueShare should sum to 100 or less across all products',
        'params': {
            'sum': sum
        }
    }


def validate_value_empty(products: list):
    def validate(values: tuple):
        index, product = values
        return len(product.get('value', [])) > 0 or {
            'level': 'warning',
            'dataPath': f".products[{index}]",
            'message': 'may not be 0'
        }

    return _filter_list_errors(map(validate, enumerate(products)))


def validate_value_0(products: list):
    def validate(values: tuple):
        index, product = values
        value = list_sum(product.get('value', [-1]), -1)
        eva = product.get('economicValueShare', 0)
        revenue = product.get('revenue', 0)
        return value != 0 or _filter_list_errors([
            eva == 0 or {
                'level': 'error',
                'dataPath': f".products[{index}].value",
                'message': 'economicValueShare must be 0 for product value 0',
                'params': {
                    'value': eva,
                    'term': product.get('term')
                }
            },
            revenue == 0 or {
                'level': 'error',
                'dataPath': f".products[{index}].value",
                'message': 'revenue must be 0 for product value 0',
                'params': {
                    'value': revenue,
                    'term': product.get('term')
                }
            }
        ])

    return _filter_list_errors(flatten(map(validate, enumerate(products))))


MAX_PRIMARY_PRODUCTS = 1


def validate_primary(products: list):
    primary = list(filter(lambda p: p.get('primary', False), products))
    return len(primary) <= MAX_PRIMARY_PRODUCTS or {
        'level': 'error',
        'dataPath': '.products',
        'message': f"only {MAX_PRIMARY_PRODUCTS} primary product allowed"
    }


def _get_excreta_term(cycle: dict):
    product = find_primary_product(cycle) or {}
    term_id = product.get('term', {}).get('@id')
    term_type = product.get('term', {}).get('termType')
    lookup = download_lookup(f"{term_type}.csv")
    return product, get_table_value(lookup, 'termid', term_id, 'excreta')


def validate_excreta(cycle: dict, list_key: str = 'products'):
    primary_product, excreta = _get_excreta_term(cycle)

    def validate(values: tuple):
        index, product = values
        term_id = product.get('term', {}).get('@id')
        term_type = product.get('term', {}).get('termType')
        return term_type != TermTermType.EXCRETA.value or term_id == excreta or {
            'level': 'warning',
            'dataPath': f".{list_key}[{index}].term.@id",
            'message': 'is too generic',
            'params': {
                'product': primary_product.get('term'),
                'term': product.get('term', {}),
                'current': term_id,
                'expected': excreta
            }
        }

    return not excreta or _filter_list_errors(map(validate, enumerate(cycle.get(list_key, []))))
