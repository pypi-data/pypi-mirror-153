from hestia_earth.schema import NodeType, TermTermType
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import non_empty_list

from hestia_earth.validation.utils import _filter_list_errors, update_error_path
from .shared import validate_country

MUST_INCLUDE_ID_COL = column_name('mustIncludeId')
MUST_INCLUDE_ID_TERM_TYPES = [
    TermTermType.INORGANICFERTILIZER.value
]


def validate_must_include_id(inputs: list):
    def missingRequiredIds(term: dict):
        term_id = term.get('@id')
        lookup = download_lookup(f"{term.get('termType')}.csv")
        other_term_ids = (get_table_value(lookup, 'termid', term_id, MUST_INCLUDE_ID_COL) or '').split(',')
        return non_empty_list([
            term_id for term_id in other_term_ids if find_term_match(inputs, term_id, None) is None
        ])

    def validate(values: tuple):
        index, input = values
        term = input.get('term', {})
        should_validate = term.get('termType') in MUST_INCLUDE_ID_TERM_TYPES
        missing_ids = missingRequiredIds(term) if should_validate else []
        return len(missing_ids) == 0 or {
            'level': 'error',
            'dataPath': f".inputs[{index}]",
            'message': f"should add missing inputs: {', '.join(missing_ids)}"
        }

    return _filter_list_errors(map(validate, enumerate(inputs)))


def validate_input_country(node: dict, list_key: list):
    def validate(values: tuple):
        index, input = values
        country = input.get('country')
        error = country is None or validate_country(input)
        return error is True or update_error_path(error, list_key, index)

    return _filter_list_errors(map(validate, enumerate(node.get(list_key, []))))


def validate_related_impacts(node: dict, list_key: list, node_map: dict = {}):
    related_impacts = node_map.get(NodeType.IMPACTASSESSMENT.value)

    def validate(values: tuple):
        index, input = values
        impact_id = input.get('impactAssessment', {}).get('id')
        impact = related_impacts.get(impact_id) if impact_id else None
        related_node_id = impact.get(node.get('type').lower(), {}).get('id') if impact else None
        return related_node_id is None or related_node_id != node.get('id') or {
            'level': 'error',
            'dataPath': f".inputs[{index}].impactAssessment",
            'message': f"can not be linked to the same {node.get('type')}"
        }

    return _filter_list_errors(map(validate, enumerate(node.get(list_key, []))))
