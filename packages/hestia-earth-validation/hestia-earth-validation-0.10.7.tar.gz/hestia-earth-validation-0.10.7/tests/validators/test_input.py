import json

from tests.utils import fixtures_path
from hestia_earth.validation.utils import _group_nodes
from hestia_earth.validation.validators.input import (
    validate_must_include_id,
    validate_input_country,
    validate_related_impacts
)


def test_validate_must_include_id_valid():
    # no inputs should be valid
    assert validate_must_include_id([]) is True

    with open(f"{fixtures_path}/input/mustIncludeId/valid.json") as f:
        data = json.load(f)
    assert validate_must_include_id(data.get('nodes')) is True

    with open(f"{fixtures_path}/input/mustIncludeId/valid-multiple-ids.json") as f:
        data = json.load(f)
    assert validate_must_include_id(data.get('nodes')) is True


def test_validate_must_include_id_invalid():
    with open(f"{fixtures_path}/input/mustIncludeId/invalid.json") as f:
        data = json.load(f)
    assert validate_must_include_id(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.inputs[0]',
        'message': 'should add missing inputs: potassiumNitrateKgK2O'
    }


def test_validate_input_country_valid():
    # no inputs should be valid
    assert validate_input_country({}, 'inputs') is True

    with open(f"{fixtures_path}/input/country/valid.json") as f:
        cycle = json.load(f)
    assert validate_input_country(cycle, 'inputs') is True


def test_validate_input_country_invalid():
    with open(f"{fixtures_path}/input/country/invalid.json") as f:
        cycle = json.load(f)
    assert validate_input_country(cycle, 'inputs') == {
        'level': 'error',
        'dataPath': '.inputs[1].country',
        'message': 'must be a country'
    }


def test_validate_related_impacts_valid():
    # no inputs should be valid
    assert validate_related_impacts({}, 'inputs') is True

    with open(f"{fixtures_path}/input/impactAssessment/valid.json") as f:
        nodes = json.load(f).get('nodes')
    assert validate_related_impacts(nodes[0], 'inputs', _group_nodes(nodes)) is True


def test_validate_related_impacts_invalid():
    with open(f"{fixtures_path}/input/impactAssessment/invalid.json") as f:
        nodes = json.load(f).get('nodes')
    assert validate_related_impacts(nodes[0], 'inputs', _group_nodes(nodes)) == {
        'level': 'error',
        'dataPath': '.inputs[1].impactAssessment',
        'message': 'can not be linked to the same Cycle'
    }
