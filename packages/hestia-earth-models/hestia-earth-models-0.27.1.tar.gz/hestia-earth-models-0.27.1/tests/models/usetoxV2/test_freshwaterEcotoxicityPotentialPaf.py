from unittest.mock import patch
import json
from hestia_earth.schema import TermTermType
from tests.utils import fixtures_path, fake_new_indicator

from hestia_earth.models.usetoxV2.freshwaterEcotoxicityPotentialPaf import MODEL, TERM_ID, run, _should_run

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


def test_should_run():
    cycle = {}
    impact = {'cycle': cycle}

    # data complete => no run
    cycle['dataCompleteness'] = {'pesticidesAntibiotics': True}

    # without factors => no run
    cycle['inputs'] = []
    assert not _should_run(impact)

    # with inputs with factor => not run
    cycle['inputs'] = [{'term': {'@id': 'CAS-10004-44-1', 'termType': TermTermType.PESTICIDEAI.value}}]
    assert not _should_run(impact)

    # with value => run
    cycle['inputs'][0]['value'] = [100]
    assert _should_run(impact) is True


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run(*args):
    with open(f"{fixtures_path}/impact_assessment/emissions/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)
    with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    impact['cycle'] = cycle
    value = run(impact)
    assert value == expected
