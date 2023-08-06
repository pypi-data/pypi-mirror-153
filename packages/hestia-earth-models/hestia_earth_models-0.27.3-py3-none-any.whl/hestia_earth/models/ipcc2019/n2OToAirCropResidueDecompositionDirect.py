from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition, TermTermType
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.constant import Units, get_atomic_conversion
from hestia_earth.models.utils.dataCompleteness import _is_term_type_complete
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.blank_node import get_total_value_converted
from hestia_earth.models.utils.measurement import most_relevant_measurement_value
from hestia_earth.models.utils.ecoClimateZone import get_ecoClimateZone_lookup_value
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
        ],
        "optional": {
            "endDate": "",
            "site": {
                "@type": "Site",
                "measurements": [
                    {"@type": "Measurement", "value": "", "term.@id": "ecoClimateZone"}
                ]
            }
        }
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
FACTORS = {
    'dry': {
        'value': 0.005,
        'min': 0,
        'max': 0.011
    },
    'wet': {
        'value': 0.006,
        'min': 0.001,
        'max': 0.011
    },
    'default': {
        'value': 0.01,
        'min': 0.001,
        'max': 0.018
    }
}


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


def _is_wet(ecoClimateZone: str = None):
    return get_ecoClimateZone_lookup_value(ecoClimateZone, 'wet') == 1 if ecoClimateZone else None


def _run(N_total: float, ecoClimateZone: str = None):
    converted_N_total = N_total * get_atomic_conversion(Units.KG_N2O, Units.TO_N)
    is_wet = _is_wet(ecoClimateZone)
    factors_key = 'default' if is_wet is None else 'wet' if is_wet else 'dry'
    value = converted_N_total * FACTORS[factors_key]['value']
    min = converted_N_total * FACTORS[factors_key]['min']
    max = converted_N_total * FACTORS[factors_key]['max']
    sd = converted_N_total * (FACTORS[factors_key]['max'] - FACTORS[factors_key]['min'])/4
    return [_emission(value, min, max, sd)]


def _should_run(cycle: dict):
    term_type_complete = _is_term_type_complete(cycle, {'termType': TermTermType.CROPRESIDUE.value})

    products = [p for p in cycle.get('products', []) if p.get('term', {}).get('@id') in PRODUCT_IDS]
    N_total = list_sum(get_total_value_converted(products, 'nitrogenContent'))

    measurements = cycle.get('site', {}).get('measurements', [])
    ecoClimateZone = most_relevant_measurement_value(measurements, 'ecoClimateZone', cycle.get('endDate'))

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    term_type_complete=term_type_complete,
                    N_total=N_total,
                    ecoClimateZone=ecoClimateZone)

    should_run = all([term_type_complete, N_total > 0])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, N_total, ecoClimateZone


def run(cycle: dict):
    should_run, N_total, ecoClimateZone = _should_run(cycle)
    return _run(N_total, ecoClimateZone) if should_run else []
