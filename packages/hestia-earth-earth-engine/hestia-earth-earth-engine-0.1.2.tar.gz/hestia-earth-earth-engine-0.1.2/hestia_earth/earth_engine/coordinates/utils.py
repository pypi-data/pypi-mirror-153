import ee

from hestia_earth.earth_engine.utils import get_param, get_required_param, get_fields_from_params
from hestia_earth.earth_engine.gee_utils import (
    clean_collection, data_from_raster, data_from_raster_by_period, defaut_scale
)


def _data_from_vector(point: ee.Geometry, collection: str, params: dict):
    fields = get_fields_from_params(params)
    collection = ee.FeatureCollection(collection).filterBounds(point)
    return clean_collection(collection, fields)


def _data_from_raster(point: ee.Geometry, collection: str, params: dict):
    image = ee.Image(collection)
    scale = int(get_param(params, 'scale', defaut_scale(image)))
    reducer = get_param(params, 'reducer', 'first')
    return data_from_raster(image.clip(point), point, reducer, scale)


def _data_from_point_by_period(point: ee.Geometry, collection: str, params: dict):
    image = ee.ImageCollection(collection)
    band_name = get_required_param(params, 'band_name')
    scale = int(get_param(params, 'scale', 10))
    reducer = get_param(params, 'reducer', 'first')
    reducer_regions = get_param(params, 'reducer_regions', 'mean')
    year = str(get_param(params, 'year', 2000))
    start_date = get_param(params, 'start_date', f"{year}-01-01")
    end_date = get_param(params, 'end_date', f"{year}-12-31")
    reducer_years = get_param(params, 'reducer_years')
    return data_from_raster_by_period(
        image, point, reducer, reducer_regions, scale, band_name, start_date, end_date, reducer_years=reducer_years
    )


DATA_BY_TYPE = {
    'vector': _data_from_vector,
    'raster': _data_from_raster,
    'raster_by_period': _data_from_point_by_period
}


def load(collection: str, ee_type: str, coordinates, params: dict):
    geometry = ee.Geometry.Point(coordinates) if isinstance(coordinates, list) else coordinates
    return DATA_BY_TYPE[ee_type](geometry, collection, params)
