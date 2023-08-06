from hestia_earth.schema import IndicatorStatsDefinition, TermTermType
from hestia_earth.utils.model import filter_list_term_type

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import convert_value_from_cycle, get_product
from hestia_earth.models.utils.lookup import _factor_value
from hestia_earth.models.utils.cycle import impact_lookup_value as cycle_lookup_value
from hestia_earth.models.utils.input import sum_input_impacts
from . import MODEL

REQUIREMENTS = {
    "ImpactAssessment": {
        "cycle": {
            "@type": "Cycle",
            "dataCompleteness.pesticidesAntibiotics": "True",
            "inputs": [{"@type": "Input", "value": "", "term.termType": "pesticideAI"}]
        }
    }
}
RETURNS = {
    "Indicator": [{
        "value": "",
        "statsDefinition": "modelled"
    }]
}
LOOKUPS = {
    "emission": "pafM3DFreshwaterEcotoxicityUsetox"
}
TERM_ID = 'freshwaterEcotoxicityPotentialPaf'


def _indicator(value: float):
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def _run(impact_assessment: dict):
    cycle = impact_assessment.get('cycle', {})
    product = get_product(impact_assessment)
    pesticides_value = convert_value_from_cycle(
        product,
        cycle_lookup_value(TERM_ID, cycle.get('inputs', []), TermTermType.PESTICIDEAI, LOOKUPS['emission']),
        None
    )
    inputs_value = convert_value_from_cycle(product, sum_input_impacts(cycle.get('inputs', []), TERM_ID), None)
    debugValues(impact_assessment, model=MODEL, term=TERM_ID,
                pesticides_value=pesticides_value,
                inputs_value=inputs_value)
    return _indicator(
        (pesticides_value or 0) + (inputs_value or 0)
    ) if pesticides_value else None


def _should_run(impact_assessment: dict):
    cycle = impact_assessment.get('cycle', {})
    is_complete = cycle.get('dataCompleteness', {}).get('pesticidesAntibiotics', False)
    inputs = filter_list_term_type(cycle.get('inputs', []), TermTermType.PESTICIDEAI)
    factor_func = _factor_value(f"{TermTermType.PESTICIDEAI.value}.csv", LOOKUPS['emission'], TERM_ID)
    factors = [(i, factor_func(i)) for i in inputs]
    has_factors = len([i for i, f in factors if f is not None]) > 0
    missing_factors = [input.get('term', {}).get('@id') for input, factor in factors if factor is None]
    no_missing_factors = len(missing_factors) == 0

    logRequirements(impact_assessment, model=MODEL, term=TERM_ID,
                    is_complete=is_complete,
                    has_factors=has_factors,
                    no_missing_factors=no_missing_factors,
                    missing_factors=';'.join(missing_factors))

    should_run = all([is_complete, has_factors, no_missing_factors])
    logShouldRun(impact_assessment, MODEL, TERM_ID, should_run)
    return should_run


def run(impact_assessment: dict): return _run(impact_assessment) if _should_run(impact_assessment) else None
