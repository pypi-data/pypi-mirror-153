from hestia_earth.earth_engine.utils import get_required_param, get_param
from hestia_earth.earth_engine.gee_utils import load_geometry, is_below_max_size, MAX_AREA_SIZE
from .utils import load

GEOMETRY_BY_TYPE = {
    'FeatureCollection': lambda x: _get_geometry_by_type(x.get('features')[0]),
    'GeometryCollection': lambda x: _get_geometry_by_type(x.get('geometries')[0]),
    'Feature': lambda x: x.get('geometry'),
    'Polygon': lambda x: x,
    'MultiPolygon': lambda x: x
}


def _get_geometry_by_type(geojson): return GEOMETRY_BY_TYPE[geojson.get('type')](geojson)


def _load_single(geometry, data: dict):
    collection = get_required_param(data, 'collection')
    ee_type = get_required_param(data, 'ee_type')
    return load(collection, ee_type, geometry, data)


def _get_geometry(data: dict):
    use_centroid = str(data.get('centroid', 'false')).lower() == 'true'
    boundary = get_required_param(data, 'boundary')
    geometry = load_geometry(boundary)
    return geometry.centroid() if use_centroid else geometry


def should_run(data: dict):
    max_area = float(get_param(data, 'max_area', MAX_AREA_SIZE))
    return is_below_max_size(_get_geometry(data), max_area)


def run(data: dict):
    geometry = _get_geometry(data)
    collections = data.get('collections', [])
    return [
        _load_single(geometry, v) for v in collections
    ] if len(collections) > 0 else _load_single(geometry, data)
