from .shared import (
    validate_dates, validate_region_in_country, validate_country,
    need_validate_coordinates, validate_coordinates,
    validate_area, need_validate_area, validate_date_lt_today, validate_is_region, validate_area_size,
    validate_region_size, need_validate_region_size, validate_boundary_size, need_validate_boundary_size
)


def validate_organisation_dates(organisation: dict):
    return validate_dates(organisation) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_organisation(organisation: dict, node_map: dict = {}):
    """
    Validates a single `Organisation`.

    Parameters
    ----------
    organisation : dict
        The `Organisation` to validate.
    node_map : dict
        The list of all nodes to do cross-validation, grouped by `type` and `id`.

    Returns
    -------
    List
        The list of errors for the `Organisation`, which can be empty if no errors detected.
    """
    return [
        validate_organisation_dates(organisation),
        validate_date_lt_today(organisation, 'startDate'),
        validate_date_lt_today(organisation, 'endDate'),
        validate_country(organisation) if 'country' in organisation else True,
        validate_is_region(organisation) if 'region' in organisation else True,
        validate_region_in_country(organisation) if 'region' in organisation else True,
        validate_coordinates(organisation) if need_validate_coordinates(organisation) else True,
        validate_area(organisation) if need_validate_area(organisation) else True,
        validate_area_size(organisation),
        validate_boundary_size(organisation) if need_validate_boundary_size(organisation) else True,
        validate_region_size(organisation) if need_validate_region_size(organisation) else True
    ]
