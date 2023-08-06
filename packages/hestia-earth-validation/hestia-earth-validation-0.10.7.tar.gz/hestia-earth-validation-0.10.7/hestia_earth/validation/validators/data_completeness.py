from hestia_earth.schema import SiteSiteType, TermTermType


def _validate_site_type(data_completeness: dict, site: dict):
    key = TermTermType.EXCRETAMANAGEMENT.value
    site_type = site.get('siteType')
    return site_type != SiteSiteType.CROPLAND.value or data_completeness.get(key) is True or {
        'level': 'warning',
        'dataPath': f".dataCompleteness.{key}",
        'message': f"should be true for site of type {site_type}"
    }


def _validate_all_values(data_completeness: dict):
    values = data_completeness.values()
    return next((value for value in values if isinstance(value, bool) and value is True), False) or {
        'level': 'warning',
        'dataPath': '.dataCompleteness',
        'message': 'may not all be set to false'
    }


def validate_dataCompleteness(data_completeness: dict, site=None):
    return [
        _validate_all_values(data_completeness),
        _validate_site_type(data_completeness, site) if site else True
    ]
