from . import unittest, numpy
from .test_multi import MultiGeometryTestCase

import pytest

from shapely.errors import EmptyPartError
from shapely.geometry import LineString, MultiLineString
from shapely.geometry.base import dump_coords


class MultiLineStringTestCase(MultiGeometryTestCase):

    def test_multilinestring(self):

        # From coordinate tuples
        geom = MultiLineString((((1.0, 2.0), (3.0, 4.0)),))
        self.assertIsInstance(geom, MultiLineString)
        self.assertEqual(len(geom.geoms), 1)
        self.assertEqual(dump_coords(geom), [[(1.0, 2.0), (3.0, 4.0)]])

        # From lines
        a = LineString(((1.0, 2.0), (3.0, 4.0)))
        ml = MultiLineString([a])
        self.assertEqual(len(ml.geoms), 1)
        self.assertEqual(dump_coords(ml), [[(1.0, 2.0), (3.0, 4.0)]])

        # From another multi-line
        ml2 = MultiLineString(ml)
        self.assertEqual(len(ml2.geoms), 1)
        self.assertEqual(dump_coords(ml2), [[(1.0, 2.0), (3.0, 4.0)]])

        # Sub-geometry Access
        geom = MultiLineString([(((0.0, 0.0), (1.0, 2.0)))])
        self.assertIsInstance(geom.geoms[0], LineString)
        self.assertEqual(dump_coords(geom.geoms[0]), [(0.0, 0.0), (1.0, 2.0)])
        with self.assertRaises(IndexError):  # index out of range
            geom.geoms[1]

        # Geo interface
        self.assertEqual(geom.__geo_interface__,
                         {'type': 'MultiLineString',
                          'coordinates': (((0.0, 0.0), (1.0, 2.0)),)})

    def test_from_multilinestring_z(self):
        coords1 = [(0.0, 1.0, 2.0), (3.0, 4.0, 5.0)]
        coords2 = [(6.0, 7.0, 8.0), (9.0, 10.0, 11.0)]

        # From coordinate tuples
        ml = MultiLineString([coords1, coords2])
        copy = MultiLineString(ml)
        self.assertIsInstance(copy, MultiLineString)
        assert copy.geom_type == 'MultiLineString'
        self.assertEqual(len(copy.geoms), 2)
        self.assertEqual(dump_coords(copy.geoms[0]), coords1)
        self.assertEqual(dump_coords(copy.geoms[1]), coords2)


    @unittest.skipIf(not numpy, 'Numpy required')
    def test_numpy(self):

        from numpy import array
        from numpy.testing import assert_array_equal

        # Construct from a numpy array
        geom = MultiLineString([array(((0.0, 0.0), (1.0, 2.0)))])
        self.assertIsInstance(geom, MultiLineString)
        self.assertEqual(len(geom.geoms), 1)
        self.assertEqual(dump_coords(geom), [[(0.0, 0.0), (1.0, 2.0)]])

    def test_subgeom_access(self):
        line0 = LineString([(0.0, 1.0), (2.0, 3.0)])
        line1 = LineString([(4.0, 5.0), (6.0, 7.0)])
        self.subgeom_access_test(MultiLineString, [line0, line1])

    def test_create_multi_with_empty_component(self):
        with self.assertRaises(EmptyPartError) as exc:
            wkt = MultiLineString([
                LineString([(0, 0), (1, 1), (2, 2)]),
                LineString()
            ]).wkt

        self.assertEqual(str(exc.exception), "Can't create MultiLineString with empty component")


@pytest.mark.filterwarnings("error:An exception was ignored")  # NumPy 1.21
def test_numpy_object_array():
    np = pytest.importorskip("numpy")

    geom = MultiLineString([[[5.0, 6.0], [7.0, 8.0]]])
    ar = np.empty(1, object)
    ar[:] = [geom]
    assert ar[0] == geom
