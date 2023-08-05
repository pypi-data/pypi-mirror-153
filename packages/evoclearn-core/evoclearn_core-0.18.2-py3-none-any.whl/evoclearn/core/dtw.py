# -*- coding: utf-8 -*-
""" Implementation of the DTW algorithm between numpy arrays
"""

#TODO: Review code and comment quality...
from typing import Optional

import numpy as np
from scipy.spatial.distance import cdist


def _generate_diagonal(m: int, n: int):
    numpoints = max(m, n) * 10
    xs = np.linspace(0, m-1, numpoints)
    ys = np.linspace(0, n-1, numpoints)
    
    diag_coords = []
    for i in range(m):
        idx = np.abs(xs - i).argmin()
        diag_coords.append((i, int(round(ys[idx]))))
    for j in range(n):
        idx = np.abs(ys - j).argmin()
        diag_coords.append((int(round(xs[idx])), j))
    return sorted(set(diag_coords))


def _generate_band(m: int, n: int, r: float):
    """r = 1.0 means no limiting
    """
    diag_coords = _generate_diagonal(m, n)
    x_offset = int(r * m)
    y_offset = int(r * n)
    limit_a = []
    limit_b = []
    for i, j in diag_coords:
        i_off = i + x_offset
        j_off = j + y_offset
        if j_off < n:
            limit_a.append((i, j_off))
        if i_off < m:
            limit_b.append((i_off, j))
    return limit_a, limit_b


def align(arr: np.ndarray,
          arr2: np.ndarray,
          path_limit: Optional[float]=None,
          **kwargs):
    """DP alignment between numpy arrays
       Returns: cumdist, dist, path (corresponding sample indices)

       The functionality is based on the distance implementations
       available in scipy.spatial.distance.cdist
    """
    numframes = arr.shape[0]
    numframes2 = arr2.shape[0]
    assert arr.shape[1] == arr2.shape[1], "Num dimensions missmatch..."

    dpp = np.zeros((numframes, numframes2), dtype=np.int)
    cumdist = cdist(arr, arr2, **kwargs)
    dist = np.array(cumdist, dtype=np.float)
    cost = -1.0
    mapping = np.zeros(numframes, dtype=np.float)

    #The path limit band determines how far we can wander from the diagonal.
    #Range of (0.0; 1.0] where 1.0 would be no limit.
    if path_limit is not None and path_limit > 0.0:
        lima, limb = _generate_band(m=cumdist.shape[0], n=cumdist.shape[1], r=path_limit)
        for i, j in lima:
            cumdist[i, j] = np.inf
        for i, j in limb:
            cumdist[i, j] = np.inf
    
    dpp[0, 0] = -1

    for i in range(1, numframes):
        cumdist[i, 0] += cumdist[i-1, 0]
        dpp[i, 0] = -1

    for i in range(1, numframes2):
        cumdist[0, i] += cumdist[0, i-1]
        dpp[0, i] = 1

    for i in range(1, numframes):
        for j in range(1, numframes2):
            if cumdist[i-1, j] < cumdist[i-1, j-1]:
                if cumdist[i, j-1] < cumdist[i-1, j]:
                    cumdist[i, j] += cumdist[i, j-1]
                    dpp[i, j] = 1   #hold
                else: #horizontal best
                    cumdist[i, j] += cumdist[i-1, j]
                    dpp[i, j] = -1  #jump
            elif cumdist[i, j-1] < cumdist[i-1, j-1]:
                cumdist[i, j] += cumdist[i, j-1]
                dpp[i, j] = 1       #hold
            else:
                cumdist[i, j] += cumdist[i-1, j-1]
                dpp[i, j] = 0       #jump

    j = numframes2 - 1
    for i in range(numframes - 1, -1, -1): #n-1 downto 0
        if cost == -1:
            cost = cumdist[i, j]
        mapping[i] = j
        while dpp[i, j] == 1:
            j -= 1
        if dpp[i, j] == 0:
            j -= 1

    path = []
    for i, c in enumerate(mapping):
        c = int(c)
        if i == 0:
            path.append((i, c))
            continue
        repeating = range(path[-1][-1], c)
        if repeating:
            path.pop()
            for j in repeating:
                path.append((i-1, j))
        path.append((i, c))

    return cumdist, dist, path
