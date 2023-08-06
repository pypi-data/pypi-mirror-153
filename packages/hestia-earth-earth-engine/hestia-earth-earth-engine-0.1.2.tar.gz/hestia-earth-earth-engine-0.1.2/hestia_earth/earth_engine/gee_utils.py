import os
import ee
from functools import reduce

AREA_FIELD = 'areaKm2'
AREA_PERCENT_FIELD = 'areaKm2_percent'
MAX_AREA_SIZE = int(os.getenv('MAX_AREA_SIZE', '5000'))
GADM_COLLECTION_PREFIX = 'users/hestiaplatform/gadm36_'


def _date_year(date: str): return int(date.split('-')[0])


def _id_to_level(id: str): return id.count('.')


def load_region(gadm_id: str):
    level = _id_to_level(gadm_id)
    id = gadm_id.replace('GADM-', '')
    return ee.FeatureCollection(f"{GADM_COLLECTION_PREFIX}{level}").filterMetadata(f"GID_{level}", 'equals', id)


def defaut_scale(image: ee.Image, band_name: str = None, default: int = 1):
    try:
        band_name = band_name or image.bandNames().getInfo()[0]
    except Exception:
        ''
    return image.select(band_name).projection().nominalScale().getInfo() if band_name else default


def rename_field(before, after):
    def rename_feature(feature):
        return ee.Feature(feature.geometry(), {after: feature.get(before)})
    return rename_feature


def clean_feature(feature: ee.Feature, fields=None, empty_feature=True):
    # will set the geomtry as empty to reduce the volume of the data
    geometry = None if empty_feature else feature.geometry()
    return ee.Feature(geometry).copyProperties(feature, fields if fields is not None and len(fields) > 0 else None)


def clean_collection(collection: ee.FeatureCollection, fields=None, empty_feature=True):
    feature = clean_feature(collection.first(), fields, empty_feature)
    return ee.FeatureCollection([feature]).getInfo()


def data_from_raster(image: ee.Image, collection: ee.FeatureCollection, reducer: str, scale: int, return_info=True):
    reducer_func = getattr(ee.Reducer, reducer)
    data = image.reduceRegions(
        collection=collection,
        reducer=reducer_func(),
        scale=scale
    )
    return data.getInfo() if return_info else data


def _filter_by_date(image: ee.ImageCollection, year: int):
    return image.filter(ee.Filter.calendarRange(year, year, 'year'))


def data_from_raster_by_period(
    image: ee.ImageCollection, collection, reducer, reducer_regions, scale, band_name, start_date, end_date,
    return_info=True, reducer_years=None
):
    # filter collection between dates
    filteredCollection = image.select(band_name).filterDate(start_date, end_date)

    def _reduce(filteredImage: ee.ImageCollection, reducer_name: str = reducer) -> ee.FeatureCollection:
        reducer_regions_name = reducer_regions or reducer
        reducer_func = getattr(ee.Reducer, reducer_name)
        reducer_regions_func = getattr(ee.Reducer, reducer_regions_name)
        # reduce the image collection to one image by taking an average/sum over the images within the given time period
        return filteredImage.reduce(reducer_func()).reduceRegions(
            collection=collection,
            reducer=reducer_regions_func(),
            scale=scale
        )

    if reducer_years:
        first_col = _reduce(_filter_by_date(filteredCollection, _date_year(start_date)))
        collections = reduce(lambda prev, year: prev.merge(
            _reduce(_filter_by_date(filteredCollection, year))
        ), range(_date_year(start_date) + 1, _date_year(end_date) + 1), first_col)
        # apply the reducer for years
        reducer_years_func = getattr(ee.Reducer, reducer_years)
        dictionary = collections.reduceColumns(
            reducer=reducer_years_func(),
            selectors=[reducer_years]
        )
        # set result on first collection to always return a FeatureCollection
        image = first_col.map(lambda c: c.set(reducer_years, dictionary.get(reducer_years)))
    else:
        image = _reduce(filteredCollection)

    return image.getInfo() if return_info else image


def area_km2(geometry: ee.Geometry): return geometry.area().divide(1000 * 1000)


def add_area(region: ee.Feature): return region.set({AREA_FIELD: area_km2(region.geometry())})


def add_area_percent(region: ee.Feature, total: float):
    return region.set({AREA_PERCENT_FIELD: ee.Number(region.get(AREA_FIELD)).multiply(100).divide(total)})


def intersect(geometry): return lambda feature: feature.intersection(geometry, 1)


def clip_collection(collection: ee.FeatureCollection, geometry: ee.Geometry): return collection.map(intersect(geometry))


def _aggregate_by_area_first(collection: ee.FeatureCollection, fields: list):
    return clean_collection(collection.sort(AREA_FIELD, False), fields)


def _aggregate_by_area_all(collection: ee.FeatureCollection, fields: list):
    total_area = collection.aggregate_sum(AREA_FIELD).getInfo()
    ffields = fields + [AREA_PERCENT_FIELD]
    return collection.map(lambda f: clean_feature(add_area_percent(f, total_area), ffields)).getInfo()


AGGREGATE_AREA_BY = {
    'first': _aggregate_by_area_first,
    'all': _aggregate_by_area_all
}


def aggregate_by_area(collection: ee.FeatureCollection, fields=[], reducer='all'):
    return AGGREGATE_AREA_BY[reducer](collection.map(add_area), fields)


def is_below_max_size(geometry: ee.Geometry, max_size: float = MAX_AREA_SIZE) -> bool:
    size = area_km2(geometry).getInfo()
    return size < max_size


GEOMETRY_BY_TYPE = {
    'FeatureCollection': lambda x: _get_geometry_by_type(x.get('features')[0]),
    'GeometryCollection': lambda x: _get_geometry_by_type(x.get('geometries')[0]),
    'Feature': lambda x: x.get('geometry'),
    'Polygon': lambda x: x,
    'MultiPolygon': lambda x: x
}


def _get_geometry_by_type(geojson): return GEOMETRY_BY_TYPE[geojson.get('type')](geojson)


def load_geometry(data: dict): return ee.Geometry(_get_geometry_by_type(data))
