from hestia_earth.schema import IndicatorStatsDefinition, SiteSiteType

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_product, convert_value_from_cycle
from hestia_earth.models.utils.cycle import land_occupation_per_kg
from hestia_earth.models.utils.input import sum_input_impacts
from .utils import get_emission_factor
from . import MODEL

REQUIREMENTS = {
    "ImpactAssessment": {
        "or": {
            "country": {"@type": "Term", "termType": "region"},
            "site": {
                "@type": "Site",
                "region": {"@type": "Term", "termType": "region"}
            }
        },
        "endDate": "",
        "product": {"@type": "Term"},
        "cycle": {
            "@type": "Cycle",
            "or": [
                {
                    "@doc": "if the [cycle.functionalUnit](https://hestia.earth/schema/Cycle#functionalUnit) = 1 ha, additional properties are required",  # noqa: E501
                    "cycleDuration": "",
                    "products": [{
                        "@type": "Product",
                        "primary": "True",
                        "value": "> 0",
                        "economicValueShare": "> 0"
                    }],
                    "site": {
                        "@type": "Site",
                        "measurements": [{"@type": "Measurement", "value": "", "term.@id": "fallowCorrection"}]
                    }
                },
                {
                    "@doc": "for orchard crops, additional properties are required",
                    "inputs": [
                        {"@type": "Input", "value": "", "term.@id": "saplings"}
                    ],
                    "practices": [
                        {"@type": "Practice", "value": "", "term.@id": "nurseryDuration"},
                        {"@type": "Practice", "value": "", "term.@id": "orchardBearingDuration"},
                        {"@type": "Practice", "value": "", "term.@id": "orchardDensity"},
                        {"@type": "Practice", "value": "", "term.@id": "orchardDuration"},
                        {"@type": "Practice", "value": "", "term.@id": "rotationDuration"}
                    ]
                }
            ]
        }
    }
}
LOOKUPS = {
    "@doc": "One of (depending on `site.siteType`)",
    "region-cropland-landTransformation100years.csv": "`permanent pasture`",
    "region-forest-landTransformation100years.csv": "`permanent pasture`",
    "region-other_natural_vegetation-landTransformation100years.csv": "`permanent pasture`"
}
RETURNS = {
    "Indicator": [{
        "value": "",
        "statsDefinition": "modelled"
    }]
}
TERM_ID_CYCLE = 'landTransformationFromPermanentPasture100YearAverageDuringCycle'
TERM_ID_INPUTS = 'landTransformationFromPermanentPasture100YearAverageInputsProduction'
TERM_ID = 'landTransformationFromPermanentPasture100YearAverageDuringCycle,landTransformationFromPermanentPasture100YearAverageInputsProduction'  # noqa: E501


def _indicator(term_id: str, value: float):
    indicator = _new_indicator(term_id, MODEL)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def _run_inputs(impact_assessment: dict, product: dict):
    cycle = impact_assessment.get('cycle', {})
    value = convert_value_from_cycle(product, sum_input_impacts(cycle.get('inputs', []), TERM_ID_CYCLE))
    debugValues(impact_assessment, model=MODEL, term=TERM_ID_INPUTS,
                value=value)
    logShouldRun(impact_assessment, MODEL, TERM_ID_INPUTS, value is not None)
    return [] if value is None else [_indicator(TERM_ID_INPUTS, value)]


def _run(impact_assessment: dict, land_occupation_m2: float, factor: float):
    value = land_occupation_m2 * factor
    debugValues(impact_assessment, model=MODEL, term=TERM_ID_CYCLE,
                value=value)
    return _indicator(TERM_ID_CYCLE, value)


def _should_run(impact_assessment: dict):
    cycle = impact_assessment.get('cycle', {})
    product = get_product(impact_assessment)
    land_occupation_m2_kg = land_occupation_per_kg(MODEL, TERM_ID_CYCLE, cycle, product)
    land_transformation_factor = get_emission_factor(impact_assessment, 100, SiteSiteType.PERMANENT_PASTURE)

    logRequirements(impact_assessment, model=MODEL, term=TERM_ID_CYCLE,
                    land_occupation_m2_kg=land_occupation_m2_kg,
                    land_transformation_factor=land_transformation_factor)

    should_run = all([land_occupation_m2_kg, land_transformation_factor is not None])
    logShouldRun(impact_assessment, MODEL, TERM_ID, should_run)

    logRequirements(impact_assessment, model=MODEL, term=TERM_ID_INPUTS,
                    product=(product or {}).get('@id'))

    should_run_inputs = all([product])
    return should_run, should_run_inputs, product, land_occupation_m2_kg, land_transformation_factor


def run(impact_assessment: dict):
    should_run, should_run_inputs, product, land_occupation_m2, factor = _should_run(impact_assessment)
    return (
        [_run(impact_assessment, land_occupation_m2, factor)] if should_run else []
    ) + (
        _run_inputs(impact_assessment, product) if should_run_inputs else []
    )
