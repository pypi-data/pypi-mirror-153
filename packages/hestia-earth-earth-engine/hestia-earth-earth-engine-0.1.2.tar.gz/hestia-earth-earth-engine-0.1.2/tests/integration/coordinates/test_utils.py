import json
from tests.utils import fixtures_path, get_result

from hestia_earth.earth_engine.coordinates.utils import load


def test_load_raster_by_period():
    with open(f"{fixtures_path}/coordinates/raster-by-period.json", encoding='utf-8') as f:
        data = json.load(f)

    result = load(data.get('collection'), data.get('ee_type'), [data.get('longitude'), data.get('latitude')], data)
    assert round(get_result(result, 'mean'), 10) == 1.0355721181


def test_load_reduce_years():
    with open(f"{fixtures_path}/coordinates/reduce-years.json", encoding='utf-8') as f:
        data = json.load(f)

    result = load(data.get('collection'), data.get('ee_type'), [data.get('longitude'), data.get('latitude')], data)
    assert round(get_result(result, 'mean'), 10) == 1.3133145281


def test_load_histosol():
    with open(f"{fixtures_path}/coordinates/histosol.json", encoding='utf-8') as f:
        data = json.load(f)

    result = load(data.get('collection'), data.get('ee_type'), [data.get('longitude'), data.get('latitude')], data)
    assert round(get_result(result, 'sum'), 10) == 1.2185599804


def test_load_raster():
    with open(f"{fixtures_path}/coordinates/raster.json", encoding='utf-8') as f:
        data = json.load(f)

    result = load(data.get('collection'), data.get('ee_type'), [data.get('longitude'), data.get('latitude')], data)
    assert get_result(result, 'first') == 81


def test_load_vector():
    with open(f"{fixtures_path}/coordinates/vector.json", encoding='utf-8') as f:
        data = json.load(f)

    result = load(data.get('collection'), data.get('ee_type'), [data.get('longitude'), data.get('latitude')], data)
    assert get_result(result, 'eco_code') == 'NT0704'
