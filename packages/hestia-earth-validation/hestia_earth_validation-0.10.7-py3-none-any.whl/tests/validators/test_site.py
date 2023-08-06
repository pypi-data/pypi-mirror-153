from unittest.mock import patch
import json
from hestia_earth.schema import SiteSiteType

from tests.utils import fixtures_path
from hestia_earth.validation.validators.site import (
    validate_site, validate_site_dates, validate_site_coordinates, validate_siteType
)

class_path = 'hestia_earth.validation.validators.site'


@patch(f"{class_path}.validate_boundary_size", return_value=True)
@patch(f"{class_path}.validate_region_size", return_value=True)
@patch(f"{class_path}.validate_coordinates", return_value=True)
def test_validate_valid(*args):
    with open(f"{fixtures_path}/site/valid.json") as f:
        node = json.load(f)
    assert validate_site(node) == [True] * 29


def test_validate_site_dates_valid():
    site = {
        'startDate': '2020-01-01',
        'endDate': '2020-01-02'
    }
    assert validate_site_dates(site) is True


def test_validate_site_dates_invalid():
    site = {
        'startDate': '2020-01-02',
        'endDate': '2020-01-01'
    }
    assert validate_site_dates(site) == {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


@patch(f"{class_path}.need_validate_coordinates", return_value=True)
def test_validate_site_coordinates(*args):
    site = {'siteType': SiteSiteType.CROPLAND.value}
    assert validate_site_coordinates(site)

    site['siteType'] = SiteSiteType.SEA_OR_OCEAN.value
    assert not validate_site_coordinates(site)


@patch(f"{class_path}.fetch_data", return_value={'mean': 25})
def test_validate_siteType_valid(*args):
    site = {
        'siteType': SiteSiteType.FOREST.value,
        'latitude': 44.18753,
        'longitude': -0.62521
    }
    assert validate_siteType(site) is True

    site = {
        'siteType': SiteSiteType.CROPLAND.value,
        'latitude': 44.5096,
        'longitude': 0.40749
    }
    assert validate_siteType(site) is True


@patch(f"{class_path}.fetch_data", return_value={'mean': 30})
def test_validate_siteType_invalid(*args):
    site = {
        'siteType': SiteSiteType.CROPLAND.value,
        'latitude': 44.18753,
        'longitude': -0.62521
    }
    assert validate_siteType(site) == {
        'level': 'warning',
        'dataPath': '.siteType',
        'message': 'The coordinates you have provided are not in a known cropland '
        'area according to the MODIS Land Cover classification (MCD12Q1.006, LCCS2, bands 25, 35, 36).'
    }

    site = {
        'siteType': SiteSiteType.FOREST.value,
        'latitude': 44.5096,
        'longitude': 0.40749
    }
    assert validate_siteType(site) == {
        'level': 'warning',
        'dataPath': '.siteType',
        'message': 'The coordinates you have provided are not in a known forest '
        'area according to the MODIS Land Cover classification (MCD12Q1.006, LCCS2, bands 10, 20, 25).'
    }
