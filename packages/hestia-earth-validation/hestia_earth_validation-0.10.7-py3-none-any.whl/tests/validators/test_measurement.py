from unittest.mock import patch
import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.measurement import (
    validate_soilTexture, validate_depths, validate_value_min_max, validate_term_unique,
    validate_require_startDate_endDate, validate_with_models, validate_value_length, validate_required_depths
)

class_path = 'hestia_earth.validation.validators.measurement'


def test_validate_soilTexture_invalid():
    # 90% on same depthUpper / depthLower
    with open(f"{fixtures_path}/measurement/soilTexture/low-value.json") as f:
        data = json.load(f)
    assert validate_soilTexture(data.get('nodes')) == [
        {
            'level': 'error',
            'dataPath': '.measurements[0]',
            'message': 'sum not equal to 100% for sandContent, siltContent, clayContent'
        },
        {
            'level': 'error',
            'dataPath': '.measurements[1]',
            'message': 'sum not equal to 100% for sandContent, siltContent, clayContent'
        },
        {
            'level': 'error',
            'dataPath': '.measurements[2]',
            'message': 'sum not equal to 100% for sandContent, siltContent, clayContent'
        }
    ]

    # remove all depthUpper / depthLower
    with open(f"{fixtures_path}/measurement/soilTexture/no-depth-high-value.json") as f:
        data = json.load(f)
    assert validate_soilTexture(data.get('nodes')) == [
        {
            'level': 'error',
            'dataPath': '.measurements[0]',
            'message': 'sum not equal to 100% for sandContent, siltContent, clayContent'
        },
        {
            'level': 'error',
            'dataPath': '.measurements[1]',
            'message': 'sum not equal to 100% for sandContent, siltContent, clayContent'
        },
        {
            'level': 'error',
            'dataPath': '.measurements[2]',
            'message': 'sum not equal to 100% for sandContent, siltContent, clayContent'
        },
        {
            'level': 'error',
            'dataPath': '.measurements[3]',
            'message': 'sum not equal to 100% for sandContent, siltContent, clayContent'
        }
    ]


def test_validate_soilTexture_invalid_percent():
    with open(f"{fixtures_path}/measurement/soilTexture/percent-invalid.json") as f:
        data = json.load(f)
    assert validate_soilTexture(data.get('nodes')) == [
        {
            'level': 'error',
            'dataPath': '.measurements[0].value',
            'message': 'is outside the allowed range',
            'params': {
                'term': {
                    '@type': 'Term',
                    '@id': 'sandContent'
                },
                'range': {'min': 86, 'max': 100}
            }
        },
        {
            'level': 'error',
            'dataPath': '.measurements[4].value',
            'message': 'is outside the allowed range',
            'params': {
                'term': {
                    '@type': 'Term',
                    '@id': 'sandContent'
                },
                'range': {'min': 20, 'max': 45}
            }
        },
        {
            'level': 'error',
            'dataPath': '.measurements[6].value',
            'message': 'is outside the allowed range',
            'params': {
                'term': {
                    '@type': 'Term',
                    '@id': 'clayContent'
                },
                'range': {'min': 27, 'max': 40}
            }
        }
    ]


def test_validate_soilTexture_valid():
    # no measurements should be valid
    assert validate_soilTexture([]) is True

    # missing element same depthUpper / depthLower
    with open(f"{fixtures_path}/measurement/soilTexture/missing-soil.json") as f:
        data = json.load(f)
    assert validate_soilTexture(data.get('nodes')) is True

    # simple no depth
    with open(f"{fixtures_path}/measurement/soilTexture/no-depth-valid.json") as f:
        data = json.load(f)
    assert validate_soilTexture(data.get('nodes')) is True

    # missing at least 1 value
    with open(f"{fixtures_path}/measurement/soilTexture/missing-values.json") as f:
        data = json.load(f)
    assert validate_soilTexture(data.get('nodes')) is True

    # valid percent
    with open(f"{fixtures_path}/measurement/soilTexture/percent-valid.json") as f:
        data = json.load(f)
    assert validate_soilTexture(data.get('nodes')) is True

    # missing value - cannot validate
    with open(f"{fixtures_path}/measurement/soilTexture/percent-missing-value.json") as f:
        data = json.load(f)
    assert validate_soilTexture(data.get('nodes')) is True


def test_validate_depths_valid():
    # no measurements should be valid
    assert validate_depths([]) is True

    with open(f"{fixtures_path}/measurement/depths/valid.json") as f:
        data = json.load(f)
    assert validate_depths(data.get('nodes')) is True


def test_validate_depths_invalid():
    with open(f"{fixtures_path}/measurement/depths/invalid.json") as f:
        data = json.load(f)
    assert validate_depths(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.measurements[2].depthLower',
        'message': 'must be greater than depthUpper'
    }


def test_validate_measurement_value_valid():
    # no measurements should be valid
    assert validate_value_min_max([]) is True

    with open(f"{fixtures_path}/measurement/min-max/value-valid.json") as f:
        data = json.load(f)
    assert validate_value_min_max(data.get('nodes')) is True


def test_validate_measurement_value_invalid():
    with open(f"{fixtures_path}/measurement/min-max/value-above.json") as f:
        data = json.load(f)
    assert validate_value_min_max(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.measurements[0].value',
        'message': 'should be below 25000.0'
    }

    with open(f"{fixtures_path}/measurement/min-max/value-below.json") as f:
        data = json.load(f)
    assert validate_value_min_max(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.measurements[0].value',
        'message': 'should be above 0.0'
    }


def test_validate_term_unique_valid():
    # no measurements should be valid
    assert validate_term_unique([]) is True

    with open(f"{fixtures_path}/measurement/unique/valid.json") as f:
        data = json.load(f)
    assert validate_term_unique(data.get('nodes')) is True


def test_validate_term_unique_invalid():
    with open(f"{fixtures_path}/measurement/unique/invalid.json") as f:
        data = json.load(f)
    assert validate_term_unique(data.get('nodes')) == [{
        'level': 'error',
        'dataPath': '.measurements[0].term.name',
        'message': 'must be unique'
    }, {
        'level': 'error',
        'dataPath': '.measurements[1].term.name',
        'message': 'must be unique'
    }]


def test_validate_require_startDate_endDate_valid():
    # no measurements should be valid
    assert validate_require_startDate_endDate({'measurements': []}, 'measurements') is True

    with open(f"{fixtures_path}/measurement/startDate-endDate-required/valid.json") as f:
        data = json.load(f)
    assert validate_require_startDate_endDate(data, 'measurements') is True


def test_validate_require_startDate_endDate_invalid():
    with open(f"{fixtures_path}/measurement/startDate-endDate-required/invalid.json") as f:
        data = json.load(f)
    assert validate_require_startDate_endDate(data, 'measurements') == [{
        'level': 'error',
        'dataPath': '.measurements[0]',
        'message': "should have required property 'startDate'",
        'params': {
            'missingProperty': 'startDate'
        }
    }, {
        'level': 'error',
        'dataPath': '.measurements[0]',
        'message': "should have required property 'endDate'",
        'params': {
            'missingProperty': 'endDate'
        }
    }]


@patch(f"{class_path}.fetch_data", return_value={'mean': 1})
def test_validate_with_models_valid(*args):
    # no measurements should be valid
    assert validate_with_models({}, 'measurements') is True

    with open(f"{fixtures_path}/measurement/models/valid.json") as f:
        data = json.load(f)
    assert validate_with_models(data, 'measurements') is True


@patch(f"{class_path}.fetch_data", return_value={'mean': 1})
def test_validate_with_models_warning(*args):
    with open(f"{fixtures_path}/measurement/models/warning.json") as f:
        data = json.load(f)
    assert validate_with_models(data, 'measurements') == {
        'level': 'warning',
        'dataPath': '.measurements[0].value',
        'message': 'the measurement provided might be in error',
        'params': {
            'current': 500,
            'expected': 1000,
            'delta': 50,
            'threshold': 0.25,
            'term': {
                '@id': 'rainfallAnnual',
                '@type': 'Term',
                'name': 'Rainfall annual'
            }
        }
    }

    # with no value warning must be on blank node
    with open(f"{fixtures_path}/measurement/models/warning-no-value.json") as f:
        data = json.load(f)
    assert validate_with_models(data, 'measurements') == {
        'level': 'warning',
        'dataPath': '.measurements[0]',
        'message': 'the measurement provided might be in error',
        'params': {
            'current': 0,
            'expected': 1000,
            'delta': 100,
            'threshold': 0.25,
            'term': {
                '@id': 'rainfallAnnual',
                '@type': 'Term',
                'name': 'Rainfall annual'
            }
        }
    }


def test_validate_value_length_valid():
    # no measurements should be valid
    assert validate_value_length({}, 'measurements') is True

    with open(f"{fixtures_path}/measurement/value-length/valid.json") as f:
        data = json.load(f)
    assert validate_value_length(data, 'measurements') is True


def test_validate_value_length_invalid():
    with open(f"{fixtures_path}/measurement/value-length/invalid.json") as f:
        data = json.load(f)
    assert validate_value_length(data, 'measurements') == {
        'level': 'error',
        'dataPath': '.measurements[1].value',
        'message': 'must not contain more than 1 value'
    }


def test_validate_required_depths_valid():
    # no measurements should be valid
    assert validate_required_depths({}, 'measurements') is True

    with open(f"{fixtures_path}/measurement/required-depths/valid.json") as f:
        data = json.load(f)
    assert validate_required_depths(data, 'measurements') is True


def test_validate_required_depths_warning():
    with open(f"{fixtures_path}/measurement/required-depths/warning.json") as f:
        data = json.load(f)
    assert validate_required_depths(data, 'measurements') == [
        {
            'level': 'warning',
            'dataPath': '.measurements[3]',
            'message': 'should set both depthUpper and depthLower'
        },
        {
            'level': 'warning',
            'dataPath': '.measurements[7]',
            'message': 'should set both depthUpper and depthLower'
        }
    ]
