import json
from tests.utils import fixtures_path, get_results, get_result

from hestia_earth.earth_engine.gee_utils import load_geometry
from hestia_earth.earth_engine.boundary.utils import load


def test_load_raster_by_period():
    with open(f"{fixtures_path}/boundary/raster-by-period.json", encoding='utf-8') as f:
        data = json.load(f)

    geometry = load_geometry(data.get('boundary'))
    result = load(data.get('collection'), data.get('ee_type'), geometry, data)
    assert round(get_result(result, 'mean'), 10) == 0.7707182633


def test_load_reduce_years():
    with open(f"{fixtures_path}/boundary/reduce-years.json", encoding='utf-8') as f:
        data = json.load(f)

    geometry = load_geometry(data.get('boundary'))
    result = load(data.get('collection'), data.get('ee_type'), geometry, data)
    assert round(get_result(result, 'mean'), 10) == 0.9758098238


def test_load_raster():
    with open(f"{fixtures_path}/boundary/raster.json", encoding='utf-8') as f:
        data = json.load(f)

    geometry = load_geometry(data.get('boundary'))
    result = load(data.get('collection'), data.get('ee_type'), geometry, data)
    assert isinstance(get_result(result, 'first'), int)


def test_load_vector():
    with open(f"{fixtures_path}/boundary/vector.json", encoding='utf-8') as f:
        data = json.load(f)

    geometry = load_geometry(data.get('boundary'))
    result = load(data.get('collection'), data.get('ee_type'), geometry, data)
    assert get_result(result, 'eco_code') == 'PA0445'


def test_load_all_ecoregion():
    with open(f"{fixtures_path}/boundary/ecoregion-all.json", encoding='utf-8') as f:
        data = json.load(f)

    geometry = load_geometry(data.get('boundary'))
    result = load(data.get('collection'), data.get('ee_type'), geometry, data)
    assert get_results(result) == [
        {
            'areaKm2_percent': 2.510076859517085,
            'eco_code': 'PA0402'
        },
        {
            'areaKm2_percent': 97.48992314048292,
            'eco_code': 'PA0445'
        }
    ]
