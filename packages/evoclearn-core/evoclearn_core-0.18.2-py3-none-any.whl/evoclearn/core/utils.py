# -*- coding: utf-8 -*-

from typing import Iterable, List, Tuple, Any
from copy import deepcopy
from functools import reduce

import pandas as pd
import numpy as np

from . import (QTA_COMPLETE_PARAMS,
               CONSONANT_CONTROL_PARAMS,
               CONSONANT_TYPE_MAP)


def standard_param_order(params: Iterable[str]) -> List[str]:
    params = list(params)
    assert len(params) == len(set(params))
    out = []
    for param in QTA_COMPLETE_PARAMS:
        if param in params:
            out.append(params.pop(params.index(param)))
    out.extend(params)
    return out


def consonant_control_params(cons: str) -> Tuple[str]:
    """X-SAMPA input"""
    return CONSONANT_CONTROL_PARAMS[CONSONANT_TYPE_MAP[cons]]


def normalise_minmax(df: pd.DataFrame,
                     bounds: pd.DataFrame,
                     lb: float=-1.0,
                     ub: float=1.0,
                     inverse: bool=False) -> pd.DataFrame:
    if inverse:
        old_range = ub - lb
        new_range = bounds.loc["max"] - bounds.loc["min"]
        return ((df - lb) / old_range * new_range) + bounds.loc["min"]
    else:
        old_range = bounds.loc["max"] - bounds.loc["min"]
        new_range = ub - lb
        return ((df - bounds.loc["min"]) / old_range * new_range) + lb


def normalise_standard(df: pd.DataFrame,
                       stats: pd.DataFrame,
                       inverse: bool=False) -> pd.DataFrame:
    if inverse:
        return df * stats.loc["std"] + stats.loc["mean"]
    else:
        return (df - stats.loc["mean"]) / stats.loc["std"]


def weights_to_ints(ws, total) -> np.ndarray:
    fs = np.array(ws, dtype=np.float64)
    fs_sum = fs.sum()
    fs = fs / fs_sum * total
    fsi = fs.astype(int)
    while fsi.sum() < total:
        rems = fs - fsi
        i = rems.argmax()
        fs[i] += 1 - rems[i]
        fsi = fs.astype(int)
    return fsi


class KeepLastValue(object):
    """This can be used to keep a copy of the last value produced by an
    iterator in order for a controlling process to monitor or save
    incremental/progress data..."""

    def __init__(self, it: Iterable[Any]):
        self._it = it
        self.last_value = None

    def __iter__(self):
        for val in self._it:
            self.last_value = deepcopy(val)
            yield val


def compose_funcs(*funcs):
    """only for single argument funcs"""
    return reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)


#####
## FROM: https://github.com/bregmanstudio/voxid/blob/master/voweltimbre.py
## Author: Michael A. Casey - Bregman Media Labs, Dartmouth College, Hanover, USA
## Copyright (C) 2015, Dartmouth College, All Rights Reserved
## License: MIT
def scan_vtln_warp_factor(Y,
                          X,
                          start=0.1,
                          end=1.8,
                          warp_function="symmetric",
                          step=0.01):
    """
    Return optimal frequency warp factor between spectrum data Y and target
    spectrum X.
    Inputs:
       Y - spectrogram data to warp
       X - target spectrogram
       [start, end) - range to scan
       warp_function - which warp method to use ["symmetric"]
    Outputs:
       alpha - optimal warp factor
    """
    min_mse = np.inf
    for alpha in np.arange(start, end, step):
        Xhat = vtln(Y, warp_function, alpha)
        mse = ((X - Xhat) ** 2).mean()
        if mse < min_mse:
            min_mse = mse
            min_alpha = alpha
        #print("alpha=%.3f, mse=%.3f" % (alpha, mse))
    #print("alpha=%.3f, min_mse=%.3f" % (min_alpha, min_mse))
    return min_alpha

def vtln(frames, warp_function="symmetric", alpha=1.0):
    """
    Vocal tract length normalization via frequency warping
    Python port of David Sundermann's matlab implementation by M. Casey
    inputs:
       frames - the frequency data to warp
       warp_function - asymmetric, symmetric, power, quadratic, bilinear [asymmetric]
       alpha - the warp factor
    """
    warp_funs = {"asymmetric", "symmetric", "power", "quadratic", "bilinear"}
    if not warp_function in warp_funs:
        raise Exception("Invalid warp function")
    ## Construct warping function:
    m = len(frames[0])
    omega = (np.arange(m) + 1.0) / m * np.pi
    omega_warped = omega.copy()
    if warp_function == "asymmetric" or warp_function == "symmetric":
        omega0 = 7.0 / 8.0 * np.pi
        if warp_function == "symmetric" and alpha > 1.0:
            omega0 = 7.0 / (8.0 * alpha) * np.pi
        omega_warped[np.where(omega <= omega0)] = alpha * omega[np.where(omega <= omega0)]
        omega_warped[np.where(omega > omega0)] = alpha * omega0 + ((np.pi - alpha * omega0) / (np.pi - omega0)) * (omega[np.where(omega > omega0)] - omega0)
        omega_warped[np.where(omega_warped >= np.pi)] = np.pi - 0.00001 + 0.00001 * (omega_warped[np.where(omega_warped >= np.pi)])
    elif warp_function == "power":
        omega_warped = np.pi * (omega / np.pi) ** alpha
    elif warp_function == "quadratic":
        omega_warped = omega + alpha * (omega / np.pi - (omega / np.pi) ** 2)
    elif warp_function == "bilinear":
        z = np.exp(omega * 1j)
        omega_warped = abs(-1j * np.log((z - alpha) / (1 - alpha * z)))
    omega_warped = omega_warped / np.pi * m
    ## Warp frames:
    warped_freqs = np.zeros(frames.shape)
    for j in range(len(frames)):
        warped_frame = np.interp(omega_warped, np.arange(m) + 1, frames[j]).T
        if np.isreal(frames[j][-1]):
            warped_frame[-1] = np.real(warped_frame[-1])
        warped_frame[np.isnan(warped_frame)] = 0
        warped_freqs[j] = warped_frame
    return warped_freqs
#####
