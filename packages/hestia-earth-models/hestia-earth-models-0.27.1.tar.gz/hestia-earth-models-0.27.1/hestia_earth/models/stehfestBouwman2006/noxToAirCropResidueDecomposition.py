from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition

from hestia_earth.models.utils.cycle import get_crop_residue_on_field_N_total
from hestia_earth.models.utils.emission import _new_emission
from .noxToAirSoilFlux import _should_run, _get_value
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
            "measurements": [
                {"@type": "Measurement", "value": "", "term.@id": "totalNitrogenPerKgSoil"},
                {"@type": "Measurement", "value": "", "term.@id": "ecoClimateZone"}
            ]
        }
    }
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 2",
        "statsDefinition": "modelled"
    }]
}
LOOKUPS = {
    "ecoClimateZone": "STEHFEST_BOUWMAN_2006_NOX-N_FACTOR"
}
TERM_ID = 'noxToAirCropResidueDecomposition'
TIER = EmissionMethodTier.TIER_2.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(cycle: dict, ecoClimateZone: str, nitrogenContent: float, N_total: float):
    noxToAirSoilFlux = _get_value(cycle, ecoClimateZone, nitrogenContent, N_total, TERM_ID)
    N_crop_residue = get_crop_residue_on_field_N_total(cycle)
    return [_emission(N_crop_residue / N_total * noxToAirSoilFlux)]


def run(cycle: dict):
    should_run, ecoClimateZone, nitrogenContent, N_total = _should_run(cycle, TERM_ID, TIER)
    return _run(cycle, ecoClimateZone, nitrogenContent, N_total) if should_run else []
