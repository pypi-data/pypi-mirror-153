from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_emission

from hestia_earth.models.stehfestBouwman2006.n2OToAirSoilFlux import MODEL, TERM_ID, run, _should_run, _get_value

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


@patch(f"{class_path}.find_primary_product", return_value={'@id': 'product'})
@patch(f"{class_path}._get_crop_crouping", return_value='Cereals')
@patch(f"{class_path}.get_crop_residue_on_field_N_total", return_value=10)
@patch(f"{class_path}.most_relevant_measurement_value", return_value=0)
def test_should_run(mock_measurement, *args):
    # no measurements => no run
    cycle = {}
    should_run, *args = _should_run(cycle)
    assert not should_run

    # with measurements => run
    mock_measurement.return_value = 10
    should_run, *args = _should_run(cycle)
    assert should_run is True


def test_handle_overflow_error():
    value = _get_value({}, [10, 10, 10, 10, 1, 'Other'], 10000000)
    assert round(value) == 1131197


@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
def test_run(*args):
    with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
