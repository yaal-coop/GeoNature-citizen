#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A module to manage geometry"""

from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import asShape
from geojson import Feature

from gncitizen.utils.errors import GeonatureApiError


def geom_from_geojson(data):
    """this function transform geojson geometry into `WKB\
    <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary>`_\
    data commonly used in PostGIS geometry fields

    :param data: geojson formatted geometry
    :type data: dict

    :return: wkb geometry
    :rtype: str
    """
    try:
        geojson = asShape(data)
        geom = from_shape(geojson, srid=4326)
    except Exception:
        # FIXME: define ValidationError
        # raise ValidationError("Can't convert geojson geometry to wkb")
        raise GeonatureApiError("Can't convert geojson geometry to wkb")
    return geom


def get_geojson_feature(wkb):
    """ return a geojson feature from WKB

    :param wkb: wkb geometry
    :type wkb: str

    :return: geojson
    :rtype: dict
    """
    geometry = to_shape(wkb)
    feature = Feature(geometry=geometry, properties={})
    return feature
