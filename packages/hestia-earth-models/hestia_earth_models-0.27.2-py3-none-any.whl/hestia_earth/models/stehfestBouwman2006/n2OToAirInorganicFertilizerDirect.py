from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition

from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.cycle import get_inorganic_fertilizer_N_total
from .n2OToAirSoilFlux import _get_value, _should_run
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
                {"@type": "Measurement", "value": "", "term.@id": "organicCarbonPerKgSoil"},
                {"@type": "Measurement", "value": "", "term.@id": "ecoClimateZone"},
                {"@type": "Measurement", "value": "", "term.@id": "clayContent"},
                {"@type": "Measurement", "value": "", "term.@id": "sandContent"},
                {"@type": "Measurement", "value": "", "term.@id": "soilPh"}
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
    "crop": "cropGroupingStehfestBouwman",
    "ecoClimateZone": "STEHFEST_BOUWMAN_2006_N2O-N_FACTOR"
}
TERM_ID = 'n2OToAirInorganicFertilizerDirect'
TIER = EmissionMethodTier.TIER_2.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(cycle: dict, content_list_of_items: list, N_total: float):
    n2OToAirSoilFlux = _get_value(cycle, content_list_of_items, N_total, TERM_ID)
    N_iorganic_fertilizer = get_inorganic_fertilizer_N_total(cycle)
    return [_emission(N_iorganic_fertilizer / N_total * n2OToAirSoilFlux)]


def run(cycle: dict):
    should_run, N_total, content_list_of_items = _should_run(cycle, TERM_ID, TIER)
    return _run(cycle, content_list_of_items, N_total) if should_run else []
