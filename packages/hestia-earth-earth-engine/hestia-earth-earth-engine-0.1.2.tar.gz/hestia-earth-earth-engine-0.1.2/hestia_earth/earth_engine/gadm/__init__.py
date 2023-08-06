from hestia_earth.earth_engine.utils import get_param, get_required_param
from hestia_earth.earth_engine.gee_utils import MAX_AREA_SIZE, load_region, is_below_max_size
from hestia_earth.earth_engine.coordinates import _load_single as load_coordinates
from .utils import load


def _load_single(geometry, data: dict):
    collection = get_required_param(data, 'collection')
    ee_type = get_required_param(data, 'ee_type')
    return load(collection, ee_type, geometry, data)


def _load_region(geometry, data: dict):
    collections = data.get('collections', [])
    return [
        _load_single(geometry, v) for v in collections
    ] if len(collections) > 0 else _load_single(geometry, data)


def _load_centroid(point, data: dict):
    collections = data.get('collections', [])
    return [
        load_coordinates(point, v) for v in collections
    ] if len(collections) > 0 else load_coordinates(point, data)


def _get_region(data: dict):
    # required params
    try:
        gadm_id = get_required_param(data, 'gadm_id')
    except Exception:
        gadm_id = get_required_param(data, 'gadm-id')

    return load_region(gadm_id)


def should_run(data: dict):
    max_area = float(get_param(data, 'max_area', MAX_AREA_SIZE))
    # skip validation if using centroid as no size limit on coordinates
    use_centroid = str(data.get('centroid', 'false')).lower() == 'true'
    return use_centroid or is_below_max_size(_get_region(data).geometry(), max_area)


def run(data: dict):
    region = _get_region(data)
    use_centroid = str(data.get('centroid', 'false')).lower() == 'true'
    return _load_centroid(region.geometry().centroid(), data) if use_centroid else _load_region(region, data)
