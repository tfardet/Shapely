from . import unittest, shapely20_deprecated

from shapely.geometry.base import BaseGeometry, EmptyGeometry
import shapely.geometry as sgeom
from shapely.geometry.polygon import LinearRing

from shapely.geometry import MultiPolygon, mapping, shape

import pytest

from tests.conftest import shapely20_wontfix


empty_generator = lambda: iter([])

class EmptinessTestCase(unittest.TestCase):

    def test_empty_class(self):
        g = EmptyGeometry()
        self.assertTrue(g.is_empty)

    def test_empty_base(self):
        g = BaseGeometry()
        self.assertTrue(g.is_empty)

    def test_empty_point(self):
        self.assertTrue(sgeom.Point().is_empty)

    def test_empty_multipoint(self):
        self.assertTrue(sgeom.MultiPoint().is_empty)

    def test_empty_geometry_collection(self):
        self.assertTrue(sgeom.GeometryCollection().is_empty)

    def test_empty_linestring(self):
        self.assertTrue(sgeom.LineString().is_empty)
        self.assertTrue(sgeom.LineString(None).is_empty)
        self.assertTrue(sgeom.LineString([]).is_empty)
        self.assertTrue(sgeom.LineString(empty_generator()).is_empty)

    def test_empty_multilinestring(self):
        self.assertTrue(sgeom.MultiLineString([]).is_empty)

    def test_empty_polygon(self):
        self.assertTrue(sgeom.Polygon().is_empty)
        self.assertTrue(sgeom.Polygon(None).is_empty)
        self.assertTrue(sgeom.Polygon([]).is_empty)
        self.assertTrue(sgeom.Polygon(empty_generator()).is_empty)

    def test_empty_multipolygon(self):
        self.assertTrue(sgeom.MultiPolygon([]).is_empty)

    def test_empty_linear_ring(self):
        self.assertTrue(LinearRing().is_empty)
        self.assertTrue(LinearRing(None).is_empty)
        self.assertTrue(LinearRing([]).is_empty)
        self.assertTrue(LinearRing(empty_generator()).is_empty)


@shapely20_deprecated
@pytest.mark.filterwarnings("error:An exception was ignored")  # NumPy 1.21
def test_numpy_object_array():
    np = pytest.importorskip("numpy")

    geoms = [BaseGeometry(), EmptyGeometry()]
    arr = np.empty(2, object)
    arr[:] = geoms


def test_shape_empty():
    empty_mp = MultiPolygon()
    empty_json = mapping(empty_mp)
    empty_shape = shape(empty_json)
    assert empty_shape.is_empty
