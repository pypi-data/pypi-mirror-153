from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition, TermTermType
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.constant import Units, get_atomic_conversion
from hestia_earth.models.utils.dataCompleteness import _is_term_type_complete
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.blank_node import get_total_value_converted
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "dataCompleteness.cropResidue": "True",
        "products": [
            {
                "@type": "Product",
                "value": "",
                "term.@id": "aboveGroundCropResidueLeftOnField",
                "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
            },
            {
                "@type": "Product",
                "value": "",
                "term.@id": "aboveGroundCropResidueIncorporated",
                "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
            },
            {
                "@type": "Product",
                "value": "",
                "term.@id": "belowGroundCropResidue",
                "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
            }
        ]
    }
}
RETURNS = {
    "Emission": [{
        "value": "",
        "min": "",
        "max": "",
        "sd": "",
        "methodTier": "tier 1",
        "statsDefinition": "modelled",
        "methodModelDescription": "Aggregated version"
    }]
}
TERM_ID = 'n2OToAirCropResidueDecompositionDirect'
TIER = EmissionMethodTier.TIER_1.value
PRODUCT_IDS = [
    'aboveGroundCropResidueLeftOnField',
    'aboveGroundCropResidueIncorporated',
    'belowGroundCropResidue'
]


def _emission(value: float, min: float, max: float, sd: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['min'] = [min]
    emission['max'] = [max]
    emission['sd'] = [sd]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    emission['methodModelDescription'] = 'Aggregated version'
    return emission


def _run(N_total: float):
    converted_N_total = N_total * get_atomic_conversion(Units.KG_N2O, Units.TO_N)
    value = converted_N_total * 0.01
    min = converted_N_total * 0.001
    max = converted_N_total * 0.018
    sd = converted_N_total * (0.018 - 0.001)/4
    return [_emission(value, min, max, sd)]


def _should_run(cycle: dict):
    term_type_complete = _is_term_type_complete(cycle, {'termType': TermTermType.CROPRESIDUE.value})

    products = [p for p in cycle.get('products', []) if p.get('term', {}).get('@id') in PRODUCT_IDS]
    N_total = list_sum(get_total_value_converted(products, 'nitrogenContent'))

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    term_type_complete=term_type_complete,
                    N_total=N_total)

    should_run = all([term_type_complete, N_total > 0])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, N_total


def run(cycle: dict):
    should_run, N_total = _should_run(cycle)
    return _run(N_total) if should_run else []
