from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_emission, FLOODED_RICE_TERMS

from hestia_earth.models.pooreNemecek2018.no3ToGroundwaterCropResidueDecomposition import MODEL, TERM_ID, run

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


@patch(f"hestia_earth.models.{MODEL}.no3ToGroundwaterSoilFlux.get_rice_paddy_terms", return_value=FLOODED_RICE_TERMS)
@patch(f"hestia_earth.models.{MODEL}.no3ToGroundwaterSoilFlux.get_max_rooting_depth", return_value=0.9)
@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
def test_run(*args):
    with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
