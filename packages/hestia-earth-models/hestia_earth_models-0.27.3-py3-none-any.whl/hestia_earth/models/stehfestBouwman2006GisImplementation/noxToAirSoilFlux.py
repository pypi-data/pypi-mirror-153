from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.cycle import (
    get_crop_residue_on_field_N_total, get_excreta_N_total,
    get_organic_fertilizer_N_total, get_inorganic_fertilizer_N_total
)
from hestia_earth.models.utils.emission import _new_emission
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "dataCompleteness.products": "",
        "dataCompleteness.cropResidue": "True",
        "dataCompleteness.fertilizer": "",
        "products": [{
            "@type": "Product",
            "value": "",
            "term.termType": ["cropResidue", "excreta"],
            "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
        }],
        "inputs": [{
            "@type": "Input",
            "value": "",
            "term.units": ["kg", "kg N"],
            "term.termType": ["organicFertilizer", "inorganicFertilizer", "excreta"],
            "optional": {
                "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
            }
        }],
        "site": {
            "@type": "Site",
            "country": {"@type": "Term", "termType": "region"}
        }
    }
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 1",
        "statsDefinition": "modelled"
    }]
}
LOOKUPS = {
    "region": "EF_NOX"
}
TERM_ID = 'noxToAirSoilFlux'
TIER = EmissionMethodTier.TIER_1.value


def _should_run(cycle: dict, term=TERM_ID, tier=TIER):
    country = cycle.get('site', {}).get('country', {})

    N_crop_residue = get_crop_residue_on_field_N_total(cycle)
    N_organic_fertilizer = get_organic_fertilizer_N_total(cycle)
    N_inorganic_fertilizer = get_inorganic_fertilizer_N_total(cycle)
    N_excreta = get_excreta_N_total(cycle)
    N_total = sum([
        N_crop_residue,
        N_organic_fertilizer,
        N_inorganic_fertilizer,
        N_excreta
    ])

    logRequirements(cycle, model=MODEL, term=term,
                    country=country.get('@id'),
                    N_total=N_total,
                    N_crop_residue=N_crop_residue,
                    N_organic_fertilizer=N_organic_fertilizer,
                    N_inorganic_fertilizer=N_inorganic_fertilizer,
                    N_excreta=N_excreta)

    should_run = all([country, N_total > 0])
    logShouldRun(cycle, MODEL, term, should_run, methodTier=tier)
    return should_run, country, N_total


def _get_value(cycle: dict, country: dict, N_total: float, term=TERM_ID):
    noxToAirSoilFlux = safe_parse_float(get_lookup_value(country, LOOKUPS['region'], model=MODEL, term=TERM_ID))
    debugValues(cycle, model=MODEL, term=term,
                noxToAirSoilFlux=noxToAirSoilFlux,
                N_total=N_total)
    return noxToAirSoilFlux * N_total


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(cycle: dict, country: dict, N_total: float):
    value = _get_value(cycle, country, N_total)
    return [_emission(value)]


def run(cycle: dict):
    should_run, country, N_total = _should_run(cycle)
    return _run(cycle, country, N_total) if should_run else []
