from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition
from hestia_earth.utils.tools import list_sum, safe_parse_float

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.input import get_total_nitrogen
from hestia_earth.models.utils.product import residue_nitrogen
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "or": {
            "inputs": [{
                "@type": "Input",
                "value": "",
                "term.units": ["kg", "kg N"],
                "optional": {
                    "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
                }
            }],
            "products": [{
                "@type": "Product",
                "value": "",
                "term.termType": "cropResidue",
                "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
            }]
        },
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
    residue = residue_nitrogen(cycle.get('products', []))
    N_total = list_sum(get_total_nitrogen(cycle.get('inputs', [])) + [residue])

    logRequirements(cycle, model=MODEL, term=term,
                    country=country.get('@id'),
                    residue=residue,
                    N_total=N_total)

    should_run = all([country, N_total > 0])
    logShouldRun(cycle, MODEL, term, should_run, methodTier=tier)
    return should_run, country, N_total, residue


def _get_value(cycle: dict, country: dict, N_total: float, term=TERM_ID):
    value = safe_parse_float(get_lookup_value(country, 'EF_NOX', model=MODEL, term=TERM_ID))
    debugValues(cycle, model=MODEL, term=term,
                nox=value,
                N_total=N_total)
    return value * N_total


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
    should_run, country, N_total, *args = _should_run(cycle)
    return _run(cycle, country, N_total) if should_run else []
