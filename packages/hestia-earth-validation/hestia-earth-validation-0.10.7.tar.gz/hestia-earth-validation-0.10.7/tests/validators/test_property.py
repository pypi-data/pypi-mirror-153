import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.property import validate_valueType, validate_default_value


def test_validate_valueType_valid():
    # no properties should be valid
    assert validate_valueType({}, 'products') is True

    with open(f"{fixtures_path}/property/valueType/valid.json") as f:
        data = json.load(f)
    assert validate_valueType(data, 'products') is True


def test_validate_valueType_invalid():
    with open(f"{fixtures_path}/property/valueType/invalid.json") as f:
        data = json.load(f)
    assert validate_valueType(data, 'products') == [
        {
            'level': 'error',
            'dataPath': '.products[1].properties[0].value',
            'message': 'must be a number'
        },
        {
            'level': 'error',
            'dataPath': '.products[1].properties[1].value',
            'message': 'must be a boolean'
        }
    ]


def test_validate_default_value_valid():
    with open(f"{fixtures_path}/property/default-value/valid.json") as f:
        node = json.load(f)
    assert validate_default_value(node, 'inputs') is True

    with open(f"{fixtures_path}/property/default-value/valid-allowed-exception.json") as f:
        node = json.load(f)
    assert validate_default_value(node, 'inputs') is True


def test_validate_default_value_warning():
    with open(f"{fixtures_path}/property/default-value/warning.json") as f:
        node = json.load(f)
    assert validate_default_value(node, 'inputs') == {
        'level': 'warning',
        'dataPath': '.inputs[0].properties[0].value',
        'message': 'should be within percentage of default value',
        'params': {
            'current': 67.0,
            'default': 52.87673036,
            'percentage': 26.71,
            'threshold': 0.25
        }
    }
