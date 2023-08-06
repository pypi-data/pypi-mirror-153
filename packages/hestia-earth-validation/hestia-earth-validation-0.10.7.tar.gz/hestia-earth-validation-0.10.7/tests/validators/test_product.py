import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.product import (
    validate_economicValueShare, validate_value_empty, validate_value_0, validate_excreta, validate_primary
)


def test_validate_economicValueShare_valid():
    # no products should be valid
    assert validate_economicValueShare([]) is True

    with open(f"{fixtures_path}/product/economicValueShare/valid.json") as f:
        data = json.load(f)
    assert validate_economicValueShare(data.get('nodes')) is True


def test_validate_economicValueShare_invalid():
    with open(f"{fixtures_path}/product/economicValueShare/invalid.json") as f:
        data = json.load(f)
    assert validate_economicValueShare(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.products',
        'message': 'economicValueShare should sum to 100 or less across all products',
        'params': {
            'sum': 110
        }
    }


def test_validate_value_empty_valid():
    # no products should be valid
    assert validate_value_empty([]) is True

    with open(f"{fixtures_path}/product/value/valid.json") as f:
        data = json.load(f)
    assert validate_value_empty(data.get('nodes')) is True


def test_validate_value_empty_warning():
    with open(f"{fixtures_path}/product/value/value-empty/warning.json") as f:
        data = json.load(f)
    assert validate_value_empty(data.get('nodes')) == {
        'level': 'warning',
        'dataPath': '.products[1]',
        'message': 'may not be 0'
    }


def test_validate_value_0_valid():
    # no products should be valid
    assert validate_value_0([]) is True

    with open(f"{fixtures_path}/product/value/valid.json") as f:
        data = json.load(f)
    assert validate_value_0(data.get('nodes')) is True


def test_validate_value_0_error():
    with open(f"{fixtures_path}/product/value/value-0/error.json") as f:
        data = json.load(f)
    assert validate_value_0(data.get('nodes')) == [
        {
            'level': 'error',
            'dataPath': '.products[1].value',
            'message': 'economicValueShare must be 0 for product value 0',
            'params': {
                'value': 100,
                'term': {
                    "@type": "Term",
                    "name": "Generic Crop, grain",
                    "@id": "genericCropGrain"
                }
            }
        },
        {
            'level': 'error',
            'dataPath': '.products[1].value',
            'message': 'revenue must be 0 for product value 0',
            'params': {
                'value': 100,
                'term': {
                    "@type": "Term",
                    "name": "Generic Crop, grain",
                    "@id": "genericCropGrain"
                }
            }
        }
    ]


def test_validate_excreta_valid():
    # no products should be valid
    assert validate_excreta({}) is True

    with open(f"{fixtures_path}/product/excreta/valid.json") as f:
        data = json.load(f)
    assert validate_excreta(data) is True

    with open(f"{fixtures_path}/product/excreta/valid-no-excreta.json") as f:
        data = json.load(f)
    assert validate_excreta(data) is True


def test_validate_excreta_warning():
    with open(f"{fixtures_path}/product/excreta/warning.json") as f:
        data = json.load(f)
    assert validate_excreta(data) == {
        'level': 'warning',
        'dataPath': '.products[1].term.@id',
        'message': 'is too generic',
        'params': {
            'product': {
                '@type': 'Term',
                '@id': 'meatChickenLiveweight',
                'termType': 'animalProduct'
            },
            'term': {
                '@type': 'Term',
                '@id': 'excretaKgN',
                'termType': 'excreta'
            },
            'current': 'excretaKgN',
            'expected': 'excretaPoultryKgN'
        }
    }


def test_validate_primary_valid():
    # no products should be valid
    assert validate_primary([]) is True

    with open(f"{fixtures_path}/product/primary/valid.json") as f:
        data = json.load(f)
    assert validate_primary(data.get('nodes')) is True


def test_validate_primary_error():
    with open(f"{fixtures_path}/product/primary/invalid.json") as f:
        data = json.load(f)
    assert validate_primary(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.products',
        'message': 'only 1 primary product allowed'
    }
