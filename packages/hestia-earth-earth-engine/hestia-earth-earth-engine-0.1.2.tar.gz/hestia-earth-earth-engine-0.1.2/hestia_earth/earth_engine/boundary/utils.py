import ee

from hestia_earth.earth_engine.utils import get_param, get_required_param, get_fields_from_params
from hestia_earth.earth_engine.gee_utils import (
    rename_field, clean_collection, aggregate_by_area, data_from_raster, data_from_raster_by_period, clip_collection,
    defaut_scale
)


def _data_from_vector(geometry: ee.Geometry, collection: str, params: dict):
    fields = get_fields_from_params(params)
    reducer = get_param(params, 'reducer', 'first')
    collection = ee.FeatureCollection(collection).filterBounds(geometry)
    return aggregate_by_area(clip_collection(collection, geometry), fields, reducer)


def _data_from_raster(geometry: ee.Geometry, collection: str, params: dict):
    image = ee.Image(collection)
    scale = int(get_param(params, 'scale', defaut_scale(image)))
    reducer = get_param(params, 'reducer', 'first')
    fields = get_fields_from_params(params)
    field = fields[0] if len(fields) == 1 else None
    data = data_from_raster(image, geometry, reducer, scale, False)
    return clean_collection(data.map(rename_field(reducer, field)) if field else data)


def _data_from_raster_by_period(geometry: ee.Geometry, collection: str, params: dict):
    image = ee.ImageCollection(collection)
    band_name = get_required_param(params, 'band_name')
    scale = int(get_param(params, 'scale', 10))
    reducer = get_param(params, 'reducer', 'first')
    reducer_regions = get_param(params, 'reducer_regions', 'mean')
    year = str(get_param(params, 'year', 2000))
    start_date = get_param(params, 'start_date', f"{year}-01-01")
    end_date = get_param(params, 'end_date', f"{year}-12-31")
    reducer_years = get_param(params, 'reducer_years')
    fields = get_fields_from_params(params)
    field = fields[0] if len(fields) == 1 else None
    data = data_from_raster_by_period(
        image, geometry, reducer, reducer_regions, scale, band_name, start_date, end_date, False,
        reducer_years=reducer_years
    )
    return clean_collection(data.map(rename_field(reducer_regions, field)) if field else data)


DATA_BY_TYPE = {
    'vector': _data_from_vector,
    'raster': _data_from_raster,
    'raster_by_period': _data_from_raster_by_period
}


def load(collection: str, ee_type: str, geometry: ee.Geometry, params: dict):
    return DATA_BY_TYPE[ee_type](geometry, collection, params)
