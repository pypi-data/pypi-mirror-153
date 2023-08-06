import json
from tests.utils import fixtures_path, get_result

from hestia_earth.earth_engine.gee_utils import load_region
from hestia_earth.earth_engine.gadm.utils import load


def test_load_raster_by_period():
    with open(f"{fixtures_path}/gadm/raster-by-period.json", encoding='utf-8') as f:
        data = json.load(f)

    region = load_region(data.get('gadm_id'))
    result = load(data.get('collection'), data.get('ee_type'), region, data)
    assert round(get_result(result, 'mean'), 10) == 0.1705916511


def test_load_reduce_years():
    with open(f"{fixtures_path}/gadm/reduce-years.json", encoding='utf-8') as f:
        data = json.load(f)

    region = load_region(data.get('gadm_id'))
    result = load(data.get('collection'), data.get('ee_type'), region, data)
    assert round(get_result(result, 'mean'), 10) == 0.2302398705


def test_load_histosol():
    with open(f"{fixtures_path}/gadm/histosol.json", encoding='utf-8') as f:
        data = json.load(f)

    region = load_region(data.get('gadm_id'))
    result = load(data.get('collection'), data.get('ee_type'), region, data)
    assert round(get_result(result, 'sum'), 10) == 241.8813767742


def test_load_ecoClimateZone():
    with open(f"{fixtures_path}/gadm/ecoClimateZone.json", encoding='utf-8') as f:
        data = json.load(f)

    region = load_region(data.get('gadm_id'))
    result = load(data.get('collection'), data.get('ee_type'), region, data)
    assert get_result(result, 'mode') == 11


def test_load_raster():
    with open(f"{fixtures_path}/gadm/raster.json", encoding='utf-8') as f:
        data = json.load(f)

    region = load_region(data.get('gadm_id'))
    result = load(data.get('collection'), data.get('ee_type'), region, data)
    assert get_result(result, 'first') == 78


def test_load_vector():
    with open(f"{fixtures_path}/gadm/vector.json", encoding='utf-8') as f:
        data = json.load(f)

    region = load_region(data.get('gadm_id'))
    result = load(data.get('collection'), data.get('ee_type'), region, data)
    assert get_result(result, 'eco_code') == 'AA1309'
