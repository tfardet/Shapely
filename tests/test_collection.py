from shapely import wkt

from shapely.geometry import LineString
from shapely.geometry.collection import GeometryCollection
from shapely.geometry import shape

import pytest


@pytest.fixture()
def geometrycollection_geojson():
    return {"type": "GeometryCollection", "geometries": [
        {"type": "Point", "coordinates": (0, 3, 0)},
        {"type": "LineString", "coordinates": ((2, 0), (1, 0))}
    ]}


@pytest.mark.parametrize('geom', [
    GeometryCollection(),
    shape({"type": "GeometryCollection", "geometries": []}),
    shape({"type": "GeometryCollection", "geometries": [
        {"type": "Point", "coordinates": ()},
        {"type": "LineString", "coordinates": (())}
    ]}),
    wkt.loads('GEOMETRYCOLLECTION EMPTY'),
])
def test_empty(geom):
    assert geom.type == "GeometryCollection"
    assert geom.type == geom.geom_type
    assert geom.is_empty
    assert len(geom.geoms) == 0
    assert geom.geoms == []


def test_child_with_deleted_parent():
    # test that we can remove a collection while keeping
    # children around
    a = LineString([(0, 0), (1, 1), (1, 2), (2, 2)])
    b = LineString([(0, 0), (1, 1), (2, 1), (2, 2)])
    collection = a.intersection(b)

    child = collection.geoms[0]
    # delete parent of child
    del collection

    # access geometry, this should not seg fault as 1.2.15 did
    assert child.wkt is not None


def test_from_geojson(geometrycollection_geojson):
    geom = shape(geometrycollection_geojson)
    assert geom.geom_type == "GeometryCollection"
    assert len(geom.geoms) == 2

    geom_types = [g.geom_type for g in geom.geoms]
    assert "Point" in geom_types
    assert "LineString" in geom_types


def test_geointerface(geometrycollection_geojson):
    geom = shape(geometrycollection_geojson)
    assert geom.__geo_interface__ == geometrycollection_geojson


def test_len_raises(geometrycollection_geojson):
    geom = shape(geometrycollection_geojson)
    with pytest.raises(TypeError):
        len(geom)


@pytest.mark.filterwarnings("error:An exception was ignored")  # NumPy 1.21
def test_numpy_object_array():
    np = pytest.importorskip("numpy")

    geom = GeometryCollection([LineString([(0, 0), (1, 1)])])
    ar = np.empty(1, object)
    ar[:] = [geom]
    assert ar[0] == geom
