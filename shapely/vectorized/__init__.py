"""Provides multi-point element-wise operations such as ``contains``."""

import numpy as np
import pygeos

from shapely.prepared import PreparedGeometry


def _construct_points(x, y):
    x, y = np.asanyarray(x), np.asanyarray(y)
    if x.shape != y.shape:
        raise ValueError('X and Y shapes must be equivalent.')

    if x.dtype != np.float64:
        x = x.astype(np.float64)
    if y.dtype != np.float64:
        y = y.astype(np.float64)

    return pygeos.points(x, y)


def contains(geometry, x, y):
    """
    Vectorized (element-wise) version of `contains` which checks whether
    multiple points are contained by a single geometry.

    Parameters
    ----------
    geometry : PreparedGeometry or subclass of BaseGeometry
        The geometry which is to be checked to see whether each point is
        contained within. The geometry will be "prepared" if it is not already
        a PreparedGeometry instance.
    x : array
        The x coordinates of the points to check.
    y : array
        The y coordinates of the points to check.

    Returns
    -------
    Mask of points contained by the given `geometry`.

    """
    points = _construct_points(x, y)
    if isinstance(geometry, PreparedGeometry):
        geometry = geometry.context
    pygeos.prepare(geometry)
    return pygeos.contains(geometry, points)


def touches(geometry, x, y):
    """
    Vectorized (element-wise) version of `touches` which checks whether
    multiple points touch the exterior of a single geometry.

    Parameters
    ----------
    geometry : PreparedGeometry or subclass of BaseGeometry
        The geometry which is to be checked to see whether each point is
        contained within. The geometry will be "prepared" if it is not already
        a PreparedGeometry instance.
    x : array
        The x coordinates of the points to check.
    y : array
        The y coordinates of the points to check.

    Returns
    -------
    Mask of points which touch the exterior of the given `geometry`.

    """
    points = _construct_points(x, y)
    if isinstance(geometry, PreparedGeometry):
        geometry = geometry.context
    pygeos.prepare(geometry)
    return pygeos.touches(geometry, points)
