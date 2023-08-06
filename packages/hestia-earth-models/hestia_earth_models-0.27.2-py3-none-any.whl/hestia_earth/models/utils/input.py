from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import find_term_match, linked_node, filter_list_term_type
from hestia_earth.utils.tools import list_sum, non_empty_list
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name

from ..log import logger
from . import _term_id, _include_methodModel, _filter_list_term_unit, _load_calculated_node
from .constant import Units
from .property import _get_nitrogen_tan_content
from .crop import get_crop_property_value_converted
from .blank_node import get_total_value


def _new_input(term, model=None):
    node = {'@type': SchemaType.INPUT.value}
    node['term'] = linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return _include_methodModel(node, model)


def load_impacts(inputs: list):
    """
    Load and return `Input`s that have an `impactAssessment`.

    Parameters
    ----------
    inputs : list
        A list of `Input`.

    Returns
    -------
    list
        The filtered list of `Input` with full `impactAssessment` node.
    """
    def _load_impact(input: dict):
        impact = input.get('impactAssessment')
        impact = _load_calculated_node(impact, SchemaType.IMPACTASSESSMENT) if impact else None
        return {**input, 'impactAssessment': impact} if impact else None

    # filter by inputs that have an impactAssessment
    return non_empty_list(map(_load_impact, inputs))


def sum_input_impacts(inputs: list, term_id: str) -> float:
    """
    Load and return the sum of the `emissionsResourceUse` value linked to each `Input`.

    Parameters
    ----------
    inputs : list
        A list of `Input`.

    Returns
    -------
    float
        The total impact of the `Input` for the `Term` or `None` if none found.
    """
    def _input_value(input: dict):
        impact = input.get('impactAssessment', {})
        indicators = impact.get('emissionsResourceUse', []) + impact.get('impacts', [])
        value = find_term_match(indicators, term_id).get('value', None)
        input_value = list_sum(input.get('value', [0]))
        logger.debug('input with impact, term=%s, input=%s, input value=%s, impact value=%s',
                     term_id, input.get('term', {}).get('@id'), input_value, value)
        return value * input_value if value is not None else None

    inputs = load_impacts(inputs)
    logger.debug('term=%s, nb inputs impact=%s', term_id, len(inputs))
    return list_sum(non_empty_list(map(_input_value, inputs)), None)


def match_lookup_value(input: dict, col_name: str, col_value):
    """
    Check if input matches lookup value.

    Parameters
    ----------
    inputs : dict
        An `Input`.
    col_name : str
        The name of the column in the lookup table.
    col_value : Any
        The cell value matching the row/column in the lookup table.

    Returns
    -------
    list
        A list of `Input`.
    """
    term_type = input.get('term', {}).get('termType')
    lookup = download_lookup(f"{term_type}.csv")
    term_id = input.get('term', {}).get('@id')
    return get_table_value(lookup, 'termid', term_id, column_name(col_name)) == col_value


def get_feed(inputs: list, prop: str = 'energyContentHigherHeatingValue'):
    inputs = _filter_list_term_unit(inputs, Units.KG)
    inputs = (
        filter_list_term_type(inputs, TermTermType.CROP) +
        filter_list_term_type(inputs, TermTermType.ANIMALPRODUCT) +
        filter_list_term_type(inputs, TermTermType.OTHER)
    )
    return list_sum([get_crop_property_value_converted(input, prop) for input in inputs])


def get_feed_nitrogen(inputs: list):
    def input_feed(input: dict):
        feed = get_feed([input], 'nitrogenContent') / 100
        return feed if feed > 0 else get_feed([input], 'crudeProteinContent') / 625

    return list_sum([input_feed(i) for i in inputs])


def get_feed_carbon(inputs: list):
    def input_feed(input: dict):
        feed = get_feed([input], 'carbonContent') / 100
        return feed if feed > 0 else get_feed([input], 'energyContentHigherHeatingValue') * 0.021

    return list_sum([input_feed(i) for i in inputs])


def total_excreta_tan(inputs: list):
    """
    Get the total excreta ammoniacal nitrogen from all the excreta inputs in `kg N` units.

    Parameters
    ----------
    inputs : list
        List of `Input`s.

    Returns
    -------
    float
        The total value as a number.
    """
    excreta = filter_list_term_type(inputs, TermTermType.EXCRETA)
    excreta = _filter_list_term_unit(excreta, Units.KG_N)
    return list_sum([
        list_sum(elem.get('value', [])) * _get_nitrogen_tan_content(elem) / 100 for elem in excreta
    ])


def total_excreta_n(inputs: list):
    """
    Get the total excreta nitrogen from all the excreta inputs in `kg N` units.

    Parameters
    ----------
    inputs : list
        List of `Input`s.

    Returns
    -------
    float
        The total value as a number.
    """
    excreta = filter_list_term_type(inputs, TermTermType.EXCRETA)
    excreta = _filter_list_term_unit(excreta, Units.KG_N)
    return list_sum(get_total_value(excreta))


def total_excreta_vs(inputs: list):
    """
    Get the total excreta volatile solid from all the excreta inputs in `kg VS` units.

    Parameters
    ----------
    inputs : list
        List of `Input`s.

    Returns
    -------
    float
        The total value as a number.
    """
    excreta = filter_list_term_type(inputs, TermTermType.EXCRETA)
    excreta = _filter_list_term_unit(excreta, Units.KG_VS)
    return list_sum(get_total_value(excreta))
