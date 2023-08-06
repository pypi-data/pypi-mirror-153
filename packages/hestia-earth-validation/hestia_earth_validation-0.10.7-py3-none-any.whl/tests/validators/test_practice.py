import json

from hestia_earth.schema import SiteSiteType

from tests.utils import fixtures_path
from hestia_earth.validation.validators.practice import (
    validate_cropResidueManagement,
    validate_longFallowPeriod,
    validate_excretaManagement,
    validate_no_tillage,
    validate_tillage_site_type,
    validate_tillage_values
)


def test_validate_cropResidueManagement_valid():
    # no practices should be valid
    assert validate_cropResidueManagement([]) is True

    with open(f"{fixtures_path}/practice/cropResidueManagement/valid.json") as f:
        data = json.load(f)
    assert validate_cropResidueManagement(data.get('nodes')) is True


def test_validate_cropResidueManagement_invalid():
    with open(f"{fixtures_path}/practice/cropResidueManagement/invalid.json") as f:
        data = json.load(f)
    assert validate_cropResidueManagement(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'value should sum to 100 or less across crop residue management practices',
        'params': {
            'sum': 110
        }
    }


def test_validate_longFallowPeriod_valid():
    # no practices should be valid
    assert validate_longFallowPeriod([]) is True

    with open(f"{fixtures_path}/practice/longFallowPeriod/valid.json") as f:
        data = json.load(f)
    assert validate_longFallowPeriod(data.get('nodes')) is True


def test_validate_longFallowPeriod_invalid():
    with open(f"{fixtures_path}/practice/longFallowPeriod/invalid.json") as f:
        data = json.load(f)
    assert validate_longFallowPeriod(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices[1].value',
        'message': 'longFallowPeriod must be lower than 5 years'
    }


def test_validate_excretaManagement_valid():
    # no practices should be valid
    assert validate_excretaManagement({}, []) is True

    with open(f"{fixtures_path}/practice/excretaManagement/valid.json") as f:
        cycle = json.load(f)
    assert validate_excretaManagement(cycle, cycle.get('practices')) is True


def test_validate_excretaManagement_invalid():
    with open(f"{fixtures_path}/practice/excretaManagement/invalid.json") as f:
        cycle = json.load(f)
    assert validate_excretaManagement(cycle, cycle.get('practices')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'an excreta input is required when using an excretaManagement practice'
    }


def test_validate_no_tillage_valid():
    # no practices should be valid
    assert validate_no_tillage([]) is True

    with open(f"{fixtures_path}/practice/noTillage/valid.json") as f:
        data = json.load(f)
    assert validate_no_tillage(data.get('nodes')) is True

    # value is not 100
    with open(f"{fixtures_path}/practice/noTillage/valid-value-not-100.json") as f:
        data = json.load(f)
    assert validate_no_tillage(data.get('nodes')) is True


def test_validate_no_tillage_invalid():
    with open(f"{fixtures_path}/practice/noTillage/invalid.json") as f:
        data = json.load(f)
    assert validate_no_tillage(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices[1]',
        'message': 'is not allowed in combination with noTillage'
    }


def test_validate_tillage_site_type_valid():
    # no practices should be valid
    assert validate_tillage_site_type([], {}) is True

    with open(f"{fixtures_path}/practice/tillage-siteType/valid.json") as f:
        cycle = json.load(f)
    assert validate_tillage_site_type(cycle.get('practices'), cycle.get('site')) is True

    # no practice but skipped termType
    with open(f"{fixtures_path}/practice/tillage-siteType/warning.json") as f:
        cycle = json.load(f)
    site = cycle.get('site')
    site['siteType'] = SiteSiteType.SEA_OR_OCEAN.value
    assert validate_tillage_site_type(cycle.get('practices'), site) is True


def test_validate_tillage_site_type_warning():
    with open(f"{fixtures_path}/practice/tillage-siteType/warning.json") as f:
        cycle = json.load(f)
    assert validate_tillage_site_type(cycle.get('practices'), cycle.get('site')) == {
        'level': 'warning',
        'dataPath': '.practices',
        'message': 'should contain a tillage practice'
    }


def test_validate_tillage_values_valid():
    # no practices should be valid
    assert validate_tillage_values([]) is True

    with open(f"{fixtures_path}/practice/tillage-values/valid-no-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) is True

    with open(f"{fixtures_path}/practice/tillage-values/valid-with-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) is True


def test_validate_tillage_values_invalid():
    with open(f"{fixtures_path}/practice/tillage-values/invalid-all-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'sum not equal to 100% for tillage practices'
    }

    with open(f"{fixtures_path}/practice/tillage-values/invalid-mixed-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'must set value for every tillage practice'
    }

    with open(f"{fixtures_path}/practice/tillage-values/invalid-no-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'can only have 1 tillage practice without a value',
        'params': {
            'current': [
                {
                    "@id": "stripTillage",
                    "@type": "Term",
                    "termType": "tillage"
                },
                {
                    "@id": "mulchTillage",
                    "@type": "Term",
                    "termType": "tillage"
                }
            ]
        }
    }
