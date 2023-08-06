from hestia_earth.schema import SiteSiteType
from hestia_earth.utils.tools import flatten

from hestia_earth.validation.gee import fetch_data
from .shared import (
    validate_dates, validate_list_dates, validate_list_dates_format, validate_list_min_max,
    validate_region_in_country, validate_country, validate_is_region, validate_coordinates, need_validate_coordinates,
    validate_area, need_validate_area, validate_list_term_percent, validate_linked_source_privacy,
    validate_list_date_lt_today, validate_date_lt_today, validate_area_size,
    validate_region_size, need_validate_region_size, validate_boundary_size, need_validate_boundary_size,
    validate_private_has_source
)
from .infrastructure import validate_lifespan
from .measurement import (
    validate_soilTexture, validate_depths, validate_required_depths, validate_value_min_max, validate_term_unique,
    validate_require_startDate_endDate, validate_with_models, validate_value_length
)
from .practice import (
    validate_cropResidueManagement, validate_longFallowPeriod, validate_no_tillage
)
from .property import (
    validate_valueType as validate_properties_valueType, validate_default_value as validate_properties_default_value
)


INLAND_TYPES = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value,
    SiteSiteType.RIVER_OR_STREAM.value,
    SiteSiteType.LAKE.value,
    SiteSiteType.ANIMAL_HOUSING.value,
    SiteSiteType.AGRI_FOOD_PROCESSOR.value,
    SiteSiteType.FOOD_RETAILER.value,
    SiteSiteType.FOREST.value,
    SiteSiteType.OTHER_NATURAL_VEGETATION.value
]

SITE_TYPES_VALID_VALUES = {
    SiteSiteType.CROPLAND.value: [25, 35, 36],
    SiteSiteType.FOREST.value: [10, 20, 25]
}


def validate_site_dates(site: dict):
    return validate_dates(site) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_site_coordinates(site: dict):
    return need_validate_coordinates(site) and site.get('siteType') in INLAND_TYPES


def validate_siteType(site: dict):
    site_type = site.get('siteType')
    values = SITE_TYPES_VALID_VALUES.get(site_type, [])
    values_str = ', '.join(map(lambda v: str(v), values))

    def validate():
        value = fetch_data(collection='MODIS/006/MCD12Q1',
                           ee_type='raster_by_period',
                           band_name='LC_Prop2',
                           year='2019',
                           latitude=site.get('latitude'),
                           longitude=site.get('longitude')).get('mean')
        return value in values

    return len(values) == 0 or validate() or {
        'level': 'warning',
        'dataPath': '.siteType',
        'message': ' '.join([
            'The coordinates you have provided are not in a known',
            site_type,
            f"area according to the MODIS Land Cover classification (MCD12Q1.006, LCCS2, bands {values_str})."
        ])
    }


def validate_site(site: dict, node_map: dict = {}):
    """
    Validates a single `Site`.

    Parameters
    ----------
    site : dict
        The `Site` to validate.
    node_map : dict
        The list of all nodes to do cross-validation, grouped by `type` and `id`.

    Returns
    -------
    List
        The list of errors for the `Site`, which can be empty if no errors detected.
    """
    return [
        validate_site_dates(site),
        validate_date_lt_today(site, 'startDate'),
        validate_date_lt_today(site, 'endDate'),
        validate_linked_source_privacy(site, 'defaultSource', node_map),
        validate_private_has_source(site, 'defaultSource'),
        validate_siteType(site) if need_validate_coordinates(site) else True,
        validate_country(site) if 'country' in site else True,
        validate_is_region(site) if 'region' in site else True,
        validate_region_in_country(site) if 'region' in site else True,
        validate_coordinates(site) if validate_site_coordinates(site) else True,
        validate_area(site) if need_validate_area(site) else True,
        validate_area_size(site),
        validate_boundary_size(site) if need_validate_boundary_size(site) else True,
        validate_region_size(site) if need_validate_region_size(site) else True
    ] + flatten([
        validate_list_dates(site, 'measurements'),
        validate_list_dates_format(site, 'measurements'),
        validate_list_date_lt_today(site, 'measurements', ['startDate', 'endDate']),
        validate_list_min_max(site, 'measurements'),
        validate_list_term_percent(site, 'measurements'),
        validate_soilTexture(site.get('measurements')),
        validate_depths(site.get('measurements')),
        validate_required_depths(site, 'measurements'),
        validate_value_min_max(site.get('measurements')),
        validate_term_unique(site.get('measurements')),
        validate_properties_default_value(site, 'measurements'),
        validate_properties_valueType(site, 'measurements'),
        validate_require_startDate_endDate(site, 'measurements'),
        validate_with_models(site, 'measurements'),
        validate_value_length(site, 'measurements')
    ] if 'measurements' in site else []) + flatten([
        validate_list_dates(site, 'infrastructure'),
        validate_list_dates_format(site, 'infrastructure'),
        validate_list_date_lt_today(site, 'infrastructure', ['startDate', 'endDate']),
        validate_lifespan(site.get('infrastructure'))
    ] if 'infrastructure' in site else []) + flatten([
        validate_list_dates(site, 'practices'),
        validate_list_dates_format(site, 'practices'),
        validate_list_date_lt_today(site, 'practices', ['startDate', 'endDate']),
        validate_list_min_max(site, 'practices'),
        validate_list_term_percent(site, 'practices'),
        validate_cropResidueManagement(site.get('practices')),
        validate_longFallowPeriod(site.get('practices')),
        validate_no_tillage(site.get('practices')),
        validate_properties_default_value(site, 'practices'),
        validate_properties_valueType(site, 'practices')
    ] if 'practices' in site else [])
