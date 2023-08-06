from os import path, listdir
from os.path import abspath, basename, dirname, isdir
from functools import reduce
from importlib import import_module
from pydash.objects import merge, merge_with, omit
from hestia_earth.schema import is_schema_type, is_type_valid
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.tools import flatten, non_empty_list

CURRENT_DIR = dirname(abspath(__file__))
IGNORE = ['', '__pycache__', '__init__.py', '_all.py', 'data', 'mocking', 'utils', 'utils.py']
PKG = '.'.join(['hestia_earth', 'models'])


def _merge_list(new_value: list, src_value: list, *args):
    return src_value + [v for v in new_value if v not in src_value]


_MERGE_BY_TYPE = {
    'list': _merge_list,
    'default': lambda *args: None  # returning None will use default "merge"
}
_MERGE_TYPE = {
    'list': lambda obj_value, src_value, *args: isinstance(obj_value, list) and isinstance(src_value, list),
    'default': lambda *args: True
}


def _merge_data(*args):
    merge_type = next((key for key, value in _MERGE_TYPE.items() if value(*args)), 'default')
    return _MERGE_BY_TYPE[merge_type](*args)


def _load_module(model: dict): return import_module(f".{model.get('model')}.{model.get('key')}", package=PKG)


def _filter_path(filepath: str): return basename(filepath) not in IGNORE


def _filter_files(values: list):
    return list(filter(lambda f: _filter_path(f.get('key')) and _filter_path(f.get('model')), values))


def _model_model(model: str): return model.replace(CURRENT_DIR, '')[1:].replace('/', '.')


def _model_id(model: dict, first_id: bool = True):
    ids = getattr(_load_module(model), 'TERM_ID', '').split(',')
    return (ids[0] if first_id else ids) if len(ids) > 0 else None


def _model_returns(model: dict): return getattr(_load_module(model), 'RETURNS', {})


def _model_requirements(model: dict): return getattr(_load_module(model), 'REQUIREMENTS', {})


def _model_requirements_cycle(model: dict):
    requirements = _model_requirements(model)
    return requirements.get('Cycle') or requirements.get('ImpactAssessment', {}).get('cycle', {})


def _model_requirements_site(model: dict):
    requirements = _model_requirements(model)
    return requirements.get('Site', {}) or \
        requirements.get('ImpactAssessment', requirements.get('Cycle', {})).get('site', {})


def _model_keys(model: str):
    def run(key: str):
        return _models(path.join(model, key)) if isdir(path.join(model, key)) else {
            'model': _model_model(model),
            'key': key.replace('.py', '')
        } if key.endswith('.py') else None
    return run


def _models(folder: str):
    files = list(filter(_filter_path, listdir(folder)))
    return _filter_files(non_empty_list(flatten(map(_model_keys(folder), files))))


def _lookup_allowed(model_term_id: str, column: str, value: str):
    term = download_hestia(model_term_id)
    lookup = download_lookup(f"{term.get('termType')}.csv")
    values = get_table_value(lookup, 'termid', model_term_id, column_name(column))
    allowed_values = (values or 'all').split(';')
    return 'all' in allowed_values or value in allowed_values


def _filter_by_termType(termType: str):
    def filter(model: dict):
        returns = _model_returns(model)
        return_type = list(returns.keys())[0] if returns else termType
        return return_type == termType
    return filter if is_type_valid(termType) else lambda *args: True


def _filter_by_tier(tier: str):
    return lambda model: tier is None or getattr(_load_module(model), 'TIER', None) == tier


def _is_model_primary_productId(model: dict, termId: str):
    products = _model_requirements_cycle(model).get('products', [])
    term_id = next((p for p in products if p.get('primary', '') == 'True'), {}).get('term.@id')
    return term_id is None or any([
        isinstance(term_id, list) and termId in term_id,
        isinstance(term_id, str) and term_id == termId
    ])


def _filter_by_productTermId(termId: str):
    # using termId allows us to also restrict by termType
    filter_by_term_type = _filter_by_productTermType(download_hestia(termId).get('termType')) if termId else None

    def filter(model: dict):
        term_id = _model_id(model)
        return all([
            _lookup_allowed(term_id, 'productTermIdsAllowed', termId) if term_id else True,
            _is_model_primary_productId(model, termId),
            filter_by_term_type(model)
        ])
    return filter if termId else lambda *args: True


def _is_model_primary_productTermType(model: dict, termType: str):
    products = _model_requirements_cycle(model).get('products', [])
    term_type = next((p for p in products if p.get('primary', '') == 'True'), {}).get('term.termType')
    return term_type is None or term_type == termType


def _filter_by_productTermType(termType: str):
    def filter(model: dict):
        term_id = _model_id(model)
        return all([
            _lookup_allowed(term_id, 'productTermTypesAllowed', termType) if term_id else True,
            _is_model_primary_productTermType(model, termType)
        ])
    return filter if termType else lambda *args: True


def _is_model_site_siteType(model: dict, siteType: str):
    site = _model_requirements_site(model)
    site_type = site.get('siteType')
    return site_type is None or site_type == siteType


def _filter_by_siteType(siteType: str):
    def filter(model: dict):
        term_id = _model_id(model)
        return all([
            _lookup_allowed(term_id, 'siteTypesAllowed', siteType) if term_id else True,
            _is_model_site_siteType(model, siteType)
        ])
    return filter if siteType else lambda *args: True


_FILTER_MODELS = {
    'termType': _filter_by_termType,
    'tier': _filter_by_tier,
    'productTermId': _filter_by_productTermId,
    'productTermType': _filter_by_productTermType,
    'siteType': _filter_by_siteType
}


def _filter_models(models: list, filters: dict):
    return reduce(lambda prev, key: list(filter(_FILTER_MODELS[key](filters[key]), prev)), filters.keys(), models)


def _split_from_requirement(key: str, value):
    term_key = key.split('.')[-1]
    return {term_key: value if isinstance(value, str) else value[0]}


def _merge_term(data: dict, key: str, value):
    data_key = 'term'
    return {
        data_key: merge(
            data.get(data_key, {'@type': 'Term', '@id': ''}), _split_from_requirement(key, value)
        )
    }


def _merge_completeness(data: dict, key: str, value):
    data_key = 'dataCompleteness'
    return {
        data_key: merge(
            data.get(data_key, {'@type': 'Completeness'}), _split_from_requirement(key, value)
        )
    }


def _merge_or(data: dict, value):
    return merge(data, value) if isinstance(value, dict) else reduce(merge, value, data)


def _remove_keys(data: dict, keys):
    for key in keys:
        del data[key]
    return data


def _clean_requirements_dict(requirements: dict):
    value = omit(requirements, '@doc', 'min', 'max')
    merge_data = {}
    omit_keys = []
    for key, v in value.items():
        new_value = _clean_requirements(v)
        if key == 'or':
            merge_data = _merge_or(merge_data, new_value)
            omit_keys.append(key)
        else:
            value[key] = new_value

        if any([key == 'optional', key == 'none']):
            omit_keys.append(key)

        # handle shorthand for nested Term
        if key.startswith('term.'):
            omit_keys.append(key)
            merge_data = merge(merge_data, _merge_term(merge_data, key, v))

        # handle shorthand for nested Completeness
        if key.startswith('dataCompleteness.'):
            omit_keys.append(key)
            merge_data = merge(merge_data, _merge_completeness(merge_data, key, v))

    return merge(_remove_keys(value, omit_keys), merge_data)


def _filter_requirement(requirement: dict):
    return not any([
        # filter Nodes or Blank Nodes with only `@type`
        isinstance(requirement, dict) and requirement.get('@type') and len(requirement.keys()) == 1,
        # filter Blank Nodes without a certain set of properties
        isinstance(requirement, dict) and is_schema_type(requirement.get('@type')) and not any([
            'value' in requirement,
            'primary' in requirement,
            'term' in requirement
        ])
    ])


def _clean_requirements(requirements: dict):
    if isinstance(requirements, list):
        # handle list of strings => set as empty
        if all([isinstance(v, str) for v in requirements]):
            return ''
        return list(filter(_filter_requirement, map(_clean_requirements, requirements)))

    if isinstance(requirements, dict):
        return _clean_requirements_dict(requirements)

    if isinstance(requirements, str):
        return requirements.replace('> 0', '')

    return requirements


def _get_requirements(model: dict):
    requirements = getattr(_load_module(model), 'REQUIREMENTS')
    node_type = list(requirements.keys())[0]
    requirements[node_type]['@type'] = node_type
    return _clean_requirements(requirements)


def _merge_requirements(all: dict, model: dict):
    requirements = _get_requirements(model)
    return merge_with(all, requirements, _merge_data)


def list_models(
    termType: str = None, tier: str = None, productTermId: str = None, productTermType: str = None, siteType: str = None
) -> list:
    """
    Return list of models present in Hestia.

    Parameters
    ----------
    termType : str
        Optional - Filter models by return `termType`.
        Possible values are: `Product`, `Input`, `Emission`, `Practice`, `Measurement`, `Indicator`, `Completeness`.
    tier : str
        Optional - Filter models by emission tier.
    productTermId : str
        Optional - Filter models running for this term `@id` only.
    productTermType : str
        Optional - Filter models running for this term `termType` only.
    siteType : str
        Optional - Filter models running for this `siteType` only.

    Returns
    -------
    list
        The models that will run based on the filters (as `{"model": model, "key": key}`).
    """
    return _filter_models(_models(CURRENT_DIR), {
        'termType': termType,
        'tier': tier,
        'productTermId': productTermId,
        **({} if productTermId else {'productTermType': productTermType}),  # productTermId will already apply
        'siteType': siteType
    })


def get_all(
    debug: bool = False,
    termType: str = None, tier: str = None, productTermId: str = None, productTermType: str = None, siteType: str = None
) -> dict:
    """
    Get the requirements to run all the models in Hestia.

    Parameters
    ----------
    debug: bool
        Optional - Print debugging information.
    termType : str
        Optional - Filter models by return `termType`.
        Possible values are: `Product`, `Input`, `Emission`, `Practice`, `Measurement`, `Indicator`, `Completeness`.
    tier : str
        Optional - Filter models by emission tier.
    productTermId : str
        Optional - Filter models running for this term `@id` only.
    productTermType : str
        Optional - Filter models running for this term `termType` only.
    siteType : str
        Optional - Filter models running for this `siteType` only.

    Returns
    -------
    dict
        The data requirements following Hestia's schema.
    """
    models = list_models(
        termType=termType, tier=tier, productTermId=productTermId, productTermType=productTermType, siteType=siteType
    )
    if debug:
        print(f"{len(models)} models found")
        for model in models:
            print('/'.join([model.get('model'), model.get('key')]))
    requirements = reduce(_merge_requirements, models, {})
    keys = list(requirements.keys())
    return requirements[keys[0]] if len(keys) == 1 else requirements


def get_single(model: str, key: str) -> dict:
    """
    Get the requirements to run a single model.

    Parameters
    ----------
    model : str
        The model name, e.g. "pooreNemecek2018".
    key
        The key for the model, e.g. "landOccupation".

    Returns
    -------
    dict
        The data requirements following Hestia's schema.
    """
    return _get_requirements({'model': model, 'key': key})


def get_term_ids(
    termType: str = None, tier: str = None, productTermId: str = None, productTermType: str = None, siteType: str = None
) -> list:
    """
    Get the `Term` `@id` that will be returned if running the models with filters.

    Parameters
    ----------
    termType : str
        Optional - Filter models by return `termType`.
        Possible values are: `Product`, `Input`, `Emission`, `Practice`, `Measurement`, `Indicator`, `Completeness`.
    tier : str
        Optional - Filter models by emission tier.
    productTermId : str
        Optional - Filter models running for this term `@id` only.
    productTermType : str
        Optional - Filter models running for this term `termType` only.
    siteType : str
        Optional - Filter models running for this `siteType` only.

    Returns
    -------
    list
        The list of `@id` the models would return if run successfully.
    """
    models = list_models(
        termType=termType, tier=tier, productTermId=productTermId, productTermType=productTermType, siteType=siteType
    )
    return list(set(flatten(non_empty_list(map(lambda model: _model_id(model, False), models)))))
