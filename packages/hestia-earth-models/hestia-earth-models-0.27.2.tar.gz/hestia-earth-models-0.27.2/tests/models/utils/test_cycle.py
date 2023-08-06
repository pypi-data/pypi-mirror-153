from unittest.mock import patch
from hestia_earth.schema import SiteSiteType

from hestia_earth.models.utils.cycle import valid_site_type, get_crop_residue_on_field_N_total

class_path = 'hestia_earth.models.utils.cycle'


def test_valid_site_type():
    site = {'siteType': SiteSiteType.CROPLAND.value}
    cycle = {'site': site}
    assert valid_site_type(cycle) is True

    cycle['site']['siteType'] = SiteSiteType.PERMANENT_PASTURE.value
    assert not valid_site_type(cycle)
    assert not valid_site_type(site, True) is True


def test_get_crop_residue_on_field_N_total_no_products():
    assert get_crop_residue_on_field_N_total({}) == 0


@patch(f"{class_path}.abg_residue_on_field_nitrogen", return_value=20)
@patch(f"{class_path}.blg_residue_nitrogen", return_value=30)
def test_get_crop_residue_on_field_N_total(*args):
    assert get_crop_residue_on_field_N_total({'dataCompleteness': {'cropResidue': True}, 'products': []}) == 50
