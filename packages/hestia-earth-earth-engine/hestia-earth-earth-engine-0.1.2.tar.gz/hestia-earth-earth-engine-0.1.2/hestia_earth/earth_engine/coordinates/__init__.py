from hestia_earth.earth_engine.utils import get_required_param, float_precision
from .utils import load


def _load_single(coordinates, data: dict):
    collection = get_required_param(data, 'collection')
    ee_type = get_required_param(data, 'ee_type')
    return load(collection, ee_type, coordinates, data)


def run(data: dict):
    # required params
    longitude = float_precision(get_required_param(data, 'longitude'))
    latitude = float_precision(get_required_param(data, 'latitude'))
    coordinates = [longitude, latitude]

    collections = data.get('collections', [])
    return [
        _load_single(coordinates, v) for v in collections
    ] if len(collections) > 0 else _load_single(coordinates, data)
