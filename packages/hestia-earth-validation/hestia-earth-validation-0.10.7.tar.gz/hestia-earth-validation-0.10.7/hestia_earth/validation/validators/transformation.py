from hestia_earth.validation.validators.shared import is_value_different
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import flatten, list_sum

from hestia_earth.validation.utils import _filter_list_errors, update_error_path
from .practice import validate_excretaManagement


def _validate_previous_term(transformations: list, index: int):
    transformation = transformations[index]
    indexes = range(len(transformations))

    def _term_index(term_id: str, max_index: int):
        return next((i for i in indexes if transformations[i].get('term', {}).get('@id') == term_id), max_index)

    term_id = transformation.get('previousTransformationTerm', {}).get('@id')
    return term_id is None or _term_index(term_id, index) < index or {
        'level': 'error',
        'dataPath': f".transformations[{index}].previousTransformationTerm",
        'message': 'must point to a previous transformation in the list'
    }


def _validate_previous_product_value(transformations: list, index: int):
    transformation = transformations[index]
    share = transformation.get('previousTransformationShare', 100)
    inputs = transformation.get('inputs', [])
    previous_transformation = transformations[index - 1]
    products = previous_transformation.get('products', [])

    def validate_input(input_index: int):
        input = list_sum(inputs[input_index].get('value', [0]))
        product = list_sum(find_term_match(products, inputs[input_index].get('term', {}).get('@id')).get('value', [0]))
        return product == 0 or not is_value_different(product, input * share / 100, 0.01) or {
            'level': 'error',
            'dataPath': f".transformations[{index}].inputs[{input_index}].value",
            'message': 'must be equal to previous product multiplied by the share'
        }

    return len(products) == 0 or _filter_list_errors(flatten(map(validate_input, range(len(inputs)))))


def validate_previous_transformation(transformations: list):
    def validate(index: int):
        return list(map(lambda func: func(transformations, index), [
            _validate_previous_term,
            _validate_previous_product_value
        ]))

    return _filter_list_errors(flatten(map(validate, range(1, len(transformations)))))


def validate_first_transformation(transformations: list):
    tr = transformations[0] if len(transformations) > 0 else None

    def validate(field: str):
        return tr.get(field) is None or {
            'level': 'error',
            'dataPath': f".transformations[0].{field}",
            'message': 'must not be set on the first transformation'
        }

    return not tr or _filter_list_errors(map(validate, ['previousTransformationTerm', 'previousTransformationShare']))


def validate_transformation_excretaManagement(transformations: list):
    def validate(values: tuple):
        index, transformation = values
        practices = transformation.get('practices', []) + [{'term': transformation.get('term')}]
        error = validate_excretaManagement(transformation, practices)
        return error is True or update_error_path(error, 'transformations', index)

    return _filter_list_errors(map(validate, enumerate(transformations)))
