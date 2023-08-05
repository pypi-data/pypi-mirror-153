# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from . import vocaltractlab as vtl
from . import (QTA_VALUE,
               QTA_SLOPE,
               QTA_TIME_CONSTANT,
               QTA_DURATION)


def target_approximation(targets: pd.DataFrame,
                         vtl_framesamples: int=vtl.FRAMESAMPLES,
                         vtl_audiosamplerate: int=vtl.AUDIO_SAMPLERATE) -> np.ndarray:
    """Calculate curve array by Target Approximation model"""
    val, slope, tau, duration = (QTA_VALUE,
                                 QTA_SLOPE,
                                 QTA_TIME_CONSTANT,
                                 QTA_DURATION)
    epsilon = 0.000000001  # arbitrary small number
    num_targets = targets.shape[0]
    target_idx = 0
    target_start_s = 0.0
    total_duration = targets[duration].sum()
    number_frames = int(total_duration * vtl_audiosamplerate) // vtl_framesamples + 1
    param_curve = np.zeros(number_frames)
    
    # first time constant
    if abs(targets[tau][target_idx]) < epsilon:
        targets[tau][target_idx] = epsilon
    a = -1.0 / targets[tau][target_idx]
    a2 = a*a
    a3 = a2*a
    a4 = a3*a

    # Coefficients for the initial target are all zero
    # -> we follow the target exactly.
    c0 = 0.0
    c1 = 0.0
    c2 = 0.0
    c3 = 0.0
    c4 = 0.0

    for i in range(number_frames):
        t_s = i * (vtl_framesamples / vtl_audiosamplerate)  # sampling time point
        while ((t_s > target_start_s + targets[duration][target_idx])
               and (target_idx < num_targets - 1)):
            # Calculate y(t) and its derivatives at the end of the prev target
            t = targets[duration][target_idx]
            t2 = t*t
            t3 = t2*t
            t4 = t3*t
            # It's important to consider the slope for f1!
            f0 = (
                np.exp(a*t)*((c0)+(c1)*t + (c2)*t2 + (c3)*t3 + (c4)*t4)
                + (
                    targets[val][target_idx]
                    + targets[duration][target_idx]
                    * targets[slope][target_idx]
                    )
                )
            f1 = (
                np.exp(a*t)*(
                    (c0*a + c1)
                    + (c1*a + 2 * c2)*t
                    + (c2*a + 3 * c3)*t2
                    + (c3*a + 4 * c4)*t3
                    + (c4*a)*t4
                    )
                + targets[slope][target_idx]
                )
            f2 = (
                np.exp(a*t)*(
                    (c0*a2 + 2 * c1*a + 2 * c2)
                    + (c1*a2 + 4 * c2*a + 6 * c3)*t
                    + (c2*a2 + 6 * c3*a + 12 * c4)*t2
                    + (c3*a2 + 8 * c4*a)*t3
                    + (c4*a2)*t4
                    )
                )
            f3 = (
                np.exp(a*t)*(
                    (c0*a3 + 3 * c1*a2 + 6 * c2*a + 6 * c3)
                    + (c1*a3 + 6 * c2*a2 + 18 * c3*a + 24 * c4)*t
                    + (c2*a3 + 9 * c3*a2 + 36 * c4*a)*t2
                    + (c3*a3 + 12 * c4*a2)*t3
                    + (c4*a3)*t4
                    )
                )
            f4 = (
                np.exp(a*t)*(
                    (c0*a4 + 4 * c1*a3 + 12 * c2*a2 + 24 * c3*a + 24 * c4)
                    + (c1*a4 + 8 * c2*a3 + 36 * c3*a2 + 96 * c4*a)*t
                    + (c2*a4 + 12 * c3*a3 + 72 * c4*a2)*t2
                    + (c3*a4 + 16 * c4*a3)*t3 + (c4*a4)*t4
                    )
                )
            # Go to the next target.
            target_start_s += targets[duration][target_idx]
            target_idx += 1
            # Calc. the coefficients for the next target based on the
            # derivatives at the end of the previous target.
            if targets[tau][target_idx] < epsilon:
                targets[tau][target_idx] = epsilon
            a = -1.0 / targets[tau][target_idx]
            a2 = a*a
            a3 = a2*a
            a4 = a3*a

            c0 = f0 - targets[val][target_idx]
            # Slope must be considered here!
            c1 = (f1 - c0*a - targets[slope][target_idx])
            c2 = (f2 - c0*a2 - c1*a * 2) / 2
            c3 = (f3 - c0*a3 - c1*a2 * 3 - c2*a * 6) / 6
            c4 = (f4 - c0*a4 - c1*a3 * 4 - c2*a2 * 12 - c3*a * 24) / 24

        t = t_s - target_start_s  #Time relative to the beginning of the target
        t2 = t*t
        t3 = t2*t
        t4 = t3*t
        param_curve[i] = (
            np.exp(a*t)*(
                (c0)+(c1)*t
                + (c2)*t2
                + (c3)*t3
                + (c4)*t4
                )
            + (
                targets[val][target_idx]
                + t*targets[slope][target_idx]
                )
            )
    return param_curve
