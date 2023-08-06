from hestia_earth.utils.tools import flatten

from .shared import (
    validate_list_min_max, validate_region_in_country, validate_country, validate_is_region,
    validate_list_term_percent, validate_linked_source_privacy, validate_date_lt_today,
    validate_list_model, validate_private_has_source
)
from .indicator import validate_characterisedIndicator_model


def validate_impact_assessment(impact_assessment: dict, node_map: dict = {}):
    """
    Validates a single `ImpactAssessment`.

    Parameters
    ----------
    impact_assessment : dict
        The `ImpactAssessment` to validate.
    node_map : dict
        The list of all nodes to do cross-validation, grouped by `type` and `id`.

    Returns
    -------
    List
        The list of errors for the `ImpactAssessment`, which can be empty if no errors detected.
    """
    return [
        validate_date_lt_today(impact_assessment, 'startDate'),
        validate_date_lt_today(impact_assessment, 'endDate'),
        validate_linked_source_privacy(impact_assessment, 'source', node_map),
        validate_private_has_source(impact_assessment, 'source'),
        validate_country(impact_assessment) if 'country' in impact_assessment else True,
        validate_is_region(impact_assessment) if 'region' in impact_assessment else True,
        validate_region_in_country(impact_assessment) if 'region' in impact_assessment else True
    ] + flatten([
        validate_list_model(impact_assessment, 'impacts'),
        validate_list_min_max(impact_assessment, 'impacts'),
        validate_list_term_percent(impact_assessment, 'impacts'),
        validate_characterisedIndicator_model(impact_assessment, 'impacts')
    ] if 'impacts' in impact_assessment else []) + flatten([
        validate_list_min_max(impact_assessment, 'emissionsResourceUse'),
        validate_list_term_percent(impact_assessment, 'emissionsResourceUse'),
        validate_characterisedIndicator_model(impact_assessment, 'emissionsResourceUse')
    ] if 'emissionsResourceUse' in impact_assessment else [])
