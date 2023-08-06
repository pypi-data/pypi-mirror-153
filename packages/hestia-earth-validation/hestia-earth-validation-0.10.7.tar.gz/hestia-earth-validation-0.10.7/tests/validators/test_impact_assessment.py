import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.impact_assessment import validate_impact_assessment


def test_validate_valid():
    with open(f"{fixtures_path}/impactAssessment/valid.json") as f:
        node = json.load(f)
    assert validate_impact_assessment(node) == [True] * 14
