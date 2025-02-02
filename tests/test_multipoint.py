from . import unittest, numpy
from .test_multi import MultiGeometryTestCase

import pytest

from shapely.errors import EmptyPartError
from shapely.geometry import Point, MultiPoint
from shapely.geometry.base import dump_coords


class MultiPointTestCase(MultiGeometryTestCase):

    def test_multipoint(self):

        # From coordinate tuples
        geom = MultiPoint(((1.0, 2.0), (3.0, 4.0)))
        self.assertEqual(len(geom.geoms), 2)
        self.assertEqual(dump_coords(geom), [[(1.0, 2.0)], [(3.0, 4.0)]])

        # From points
        geom = MultiPoint((Point(1.0, 2.0), Point(3.0, 4.0)))
        self.assertEqual(len(geom.geoms), 2)
        self.assertEqual(dump_coords(geom), [[(1.0, 2.0)], [(3.0, 4.0)]])

        # From another multi-point
        geom2 = MultiPoint(geom)
        self.assertEqual(len(geom2.geoms), 2)
        self.assertEqual(dump_coords(geom2), [[(1.0, 2.0)], [(3.0, 4.0)]])

        # Sub-geometry Access
        self.assertIsInstance(geom.geoms[0], Point)
        self.assertEqual(geom.geoms[0].x, 1.0)
        self.assertEqual(geom.geoms[0].y, 2.0)
        with self.assertRaises(IndexError):  # index out of range
            geom.geoms[2]

        # Geo interface
        self.assertEqual(geom.__geo_interface__,
                         {'type': 'MultiPoint',
                          'coordinates': ((1.0, 2.0), (3.0, 4.0))})

    @unittest.skipIf(not numpy, 'Numpy required')
    def test_multipoint_from_numpy(self):

        from numpy import array, asarray
        from numpy.testing import assert_array_equal

        # Construct from a numpy array
        geom = MultiPoint(array([[0.0, 0.0], [1.0, 2.0]]))
        self.assertIsInstance(geom, MultiPoint)
        self.assertEqual(len(geom.geoms), 2)
        self.assertEqual(dump_coords(geom), [[(0.0, 0.0)], [(1.0, 2.0)]])

    def test_subgeom_access(self):
        p0 = Point(1.0, 2.0)
        p1 = Point(3.0, 4.0)
        self.subgeom_access_test(MultiPoint, [p0, p1])

    def test_create_multi_with_empty_component(self):
        with self.assertRaises(EmptyPartError) as exc:
            wkt = MultiPoint([Point(0, 0), Point()]).wkt

        self.assertEqual(str(exc.exception), "Can't create MultiPoint with empty component")


@unittest.skipIf(not numpy, 'Numpy required')
def test_multipoint_array_coercion():
    import numpy as np

    geom = MultiPoint(((1.0, 2.0), (3.0, 4.0)))
    arr = np.array(geom)
    assert arr.ndim == 0
    assert arr.size == 1
    assert arr.dtype == np.dtype("object")
    assert arr.item() == geom


@pytest.mark.filterwarnings("error:An exception was ignored")  # NumPy 1.21
def test_numpy_object_array():
    np = pytest.importorskip("numpy")

    geom = MultiPoint(((1.0, 2.0), (3.0, 4.0)))
    ar = np.empty(1, object)
    ar[:] = [geom]
    assert ar[0] == geom


def test_len_raises():
    geom = MultiPoint([[5.0, 6.0], [7.0, 8.0]])
    with pytest.raises(TypeError):
        len(geom)
