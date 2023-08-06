import json

from hestia_earth.schema import SiteSiteType, TermTermType

from tests.utils import fixtures_path
from hestia_earth.validation.validators.data_completeness import (
    validate_dataCompleteness, _validate_all_values, _validate_site_type
)


def test_validate_dataCompleteness_valid():
    with open(f"{fixtures_path}/dataCompleteness/valid.json") as f:
        data = json.load(f)
    assert validate_dataCompleteness(data) == [True] * 2


def test_validate_all_values_valid():
    with open(f"{fixtures_path}/dataCompleteness/valid.json") as f:
        data = json.load(f)
    assert _validate_all_values(data) is True


def test_validate_all_values_warning():
    with open(f"{fixtures_path}/dataCompleteness/all-values/warning.json") as f:
        data = json.load(f)
    assert _validate_all_values(data) == {
        'level': 'warning',
        'dataPath': '.dataCompleteness',
        'message': 'may not all be set to false'
    }


def test_validate_site_type_valid():
    with open(f"{fixtures_path}/dataCompleteness/site-type/site.json") as f:
        site = json.load(f)
    with open(f"{fixtures_path}/dataCompleteness/site-type/valid.json") as f:
        data = json.load(f)
    assert _validate_site_type(data, site) is True

    # also works if siteType is not cropland
    site['siteType'] = SiteSiteType.LAKE.value
    data[TermTermType.EXCRETAMANAGEMENT.value] = False
    assert _validate_site_type(data, site) is True


def test_validate_site_type_warning():
    with open(f"{fixtures_path}/dataCompleteness/site-type/site.json") as f:
        site = json.load(f)
    with open(f"{fixtures_path}/dataCompleteness/site-type/warning.json") as f:
        data = json.load(f)
    assert _validate_site_type(data, site) == {
        'level': 'warning',
        'dataPath': f".dataCompleteness.{TermTermType.EXCRETAMANAGEMENT.value}",
        'message': 'should be true for site of type cropland'
    }
