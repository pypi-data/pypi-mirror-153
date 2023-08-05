# -*- coding: utf-8 -*-
"""Collection of lower-level functions that calculate distances between
sequences of multi-dimensional samples..."""

import numpy as np
import scipy.spatial.distance as _dist

from . import dtw as _dtw


def frame_by_frame(u: np.ndarray, v: np.ndarray, **kwargs) -> np.ndarray:
    """Frame-by-frame distance between two 2d-arrays where rows are
    observations and cols are dimensions. Returns a flat array with
    length equal to number of frames"""
    assert u.shape == v.shape
    d = np.zeros(u.shape[0], dtype=u.dtype)
    for i in range(len(d)):
        pair = np.concatenate((u[i].reshape(1, -1), v[i].reshape(1, -1)))
        d[i] = _dist.pdist(pair, **kwargs)
    return d


def dtw(u: np.ndarray, v: np.ndarray, **kwargs):
    cumdist, dist, path = _dtw.align(u, v, **kwargs)
    ui = np.zeros(len(path), dtype=np.int)
    vi = np.zeros(len(path), dtype=np.int)
    for i in range(len(path)):
        ui[i] = path[i][0]
        vi[i] = path[i][1]
    d = dist[ui, vi]
    return d, ui, vi
