# -*- coding: utf-8 -*-

"""Some constraint functions that take a Sequence and calculates the constraint
relationship, should be of the form f(x) <= 0 for a satisfied constraint.

These functions are designed to be used by external optimisers such as `skopt`
and `nlopt`.

For more convenient usage consider the filters that discard sequences based on
these functions.

"""

from typing import Any, Callable
from itertools import groupby

import numpy as np
import pandas as pd

from .. import Sequence
from .. import log
from .. import VOCALTRACT_PARAMS, GLOTTIS_PARAMS
from .. import vocaltractlab as vtl


LOGGER = log.getLogger("evl.core.constraints.generic")


#This parameter should be determined for a specific speaker file, 1.0
#here basically means unknown/no-normalisation:
DEFAULT_MAX_TRACT_AREA = 1.0 #cm2

#This parameter should be determined for a specific speaker file, this
#is an approximate value suitable for JD2:
DEFAULT_MAX_TRACT_LENGTH = 19.0 #cm

DEFAULT_UNCLOSED_TRACT_AREA_THRESHOLD = 0.1
DEFAULT_OPEN_TRACT_AREA_THRESHOLD = 0.2
DEFAULT_VOLUME_VELOCITY_THRESHOLD = 0.3
DEFAULT_SINGLE_PLACE_CLOSURE_MAX_LENGTH = 1.0 #cm


def _apply_index_slice(seq: Sequence, idx_slice):
    if idx_slice is None:
        return seq
    _seq = seq.loc[idx_slice, :]
    if _seq.empty:
        raise Exception(f"Empty sequence in constraint function (idx_slice={idx_slice})")
    return _seq


def tongue_tip_ahead_of_blade(seq: Sequence, idx_slice=None, **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    vals = []
    for i in range(len(_seq)):
        ttx = _seq.iloc[i]["TTX"]
        tbx = _seq.iloc[i]["TBX"]
        vals.append(tbx - ttx)
        LOGGER.debug("tongue_tip_ahead_of_blade:"
                     " segment=%s, TTX=%s, TBX=%s, f=%s}"
                     % (i, ttx, tbx, vals[-1]))
    return max(vals)


def tongue_blade_ahead_of_body(seq: Sequence, idx_slice=None, **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    vals = []
    for i in range(len(_seq)):
        tbx = _seq.iloc[i]["TBX"]
        tcx = _seq.iloc[i]["TCX"]
        vals.append(tcx - tbx)
        LOGGER.debug("tongue_blade_ahead_of_body:"
                     " segment=%s, TBX=%s, TCX=%s, f=%s"
                     % (i, tbx, tcx, vals[-1]))
    return max(vals)


def tongue_blade_above_body(seq: Sequence, idx_slice=None, **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    vals = []
    for i in range(len(_seq)):
        tby = _seq.iloc[i]["TBY"]
        tcy = _seq.iloc[i]["TCY"]
        vals.append(tcy - tby)
        LOGGER.debug("tongue_blade_above_body:"
                     " segment=%s, TBY=%s, TCY=%s, f=%s"
                     % (i, tby, tcy, vals[-1]))
    return max(vals)


def voiced(seq: Sequence,
           idx_slice=None,
           volume_velocity_threshold=DEFAULT_VOLUME_VELOCITY_THRESHOLD,
           **kwargs) -> float:
    """This is based on the old "voice_check" function. It uses
    VTL.vtlGetTransferFunction to obtain the volume velocity
    profile. If the profile is above volume_velocity_threshold at any
    point then the sound is deemed "voiced".
    """
    _seq = _apply_index_slice(seq, idx_slice)
    # Frequency resolution of: vtl.AUDIO_SAMPLERATE / num_spectrum_samples
    num_spectrum_samples = 2048
    for i in range(len(_seq)):
        this_frame = _seq.iloc[i]
        # DIRECT PORT FROM EVOCLEARN-RAW:
        magnitude_spectrum, phase_spectrum = vtl.transfer_function(this_frame,
                                                                   num_spectrum_samples)
        # using the log gives a divide by 0 error
        # volume = np.where(np.log10(magnitude_spectrum[:]) > volume_velocity_threshold)[0]
        # basically > 2
        mag = magnitude_spectrum[:num_spectrum_samples // 2]
        volume = np.where(mag > 10 ** volume_velocity_threshold)[0]
        # the thread for the volume velocity transfer function can be modified
        if len(volume) <= 0:
            return 1.0   # this_frame is voiceless
    return -1.0   # all frames are voiced


def tract_open(seq: Sequence,
               idx_slice=None,
               open_tract_area_threshold=DEFAULT_OPEN_TRACT_AREA_THRESHOLD,
               **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    worst_violations = []
    for i in range(len(_seq)):
        tube_areas = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes["tube_area"]
        worst_violations.append((open_tract_area_threshold - tube_areas).max())
    return max(worst_violations) / open_tract_area_threshold


def tongue_tip_closure(seq: Sequence,
                       tongue_tip_length,
                       idx_slice=None,
                       unclosed_tract_area_threshold=DEFAULT_UNCLOSED_TRACT_AREA_THRESHOLD,
                       maximum_tract_area=DEFAULT_MAX_TRACT_AREA,
                       **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    tongue_idx = pd.IndexSlice[:, "tongue"]
    violations = []
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        tongue_from_tip_to_body = tubes.loc[tongue_idx, :].iloc[::-1]
        tongue_positions_relative_to_tip = np.cumsum(tongue_from_tip_to_body["tube_length"])
        tongue_tip = tongue_from_tip_to_body.loc[tongue_positions_relative_to_tip < tongue_tip_length]["tube_area"]
        # vtl.TUBE_AREA_THRESHOLD should be called vtl.TUBE_AREA_EPSILON:
        tongue_tip_violation = (tongue_tip - vtl.TUBE_AREA_THRESHOLD).min() / maximum_tract_area
        if tongue_tip_violation > 0.0 or unclosed_tract_area_threshold is None:
            violations.append(tongue_tip_violation)
        else:
            other_than_tongue_tip = tubes.loc[tubes.index.difference(tongue_tip.index)]["tube_area"]
            other_worst_violation = (unclosed_tract_area_threshold - other_than_tongue_tip).max() / unclosed_tract_area_threshold
            violations.append(other_worst_violation)
    return max(violations)


def other_than_tongue_tip_open(seq: Sequence,
                               tongue_tip_length,
                               idx_slice=None,
                               other_open_tract_area_threshold=DEFAULT_UNCLOSED_TRACT_AREA_THRESHOLD,
                               **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    tongue_idx = pd.IndexSlice[:, "tongue"]
    worst_violations = []
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        tongue_from_tip_to_body = tubes.loc[tongue_idx, :].iloc[::-1]
        tongue_positions_relative_to_tip = np.cumsum(tongue_from_tip_to_body["tube_length"])
        tongue_tip = tongue_from_tip_to_body.loc[tongue_positions_relative_to_tip < tongue_tip_length]["tube_area"]
        other_than_tongue_tip = tubes.loc[tubes.index.difference(tongue_tip.index)]["tube_area"]
        worst_violations.append((other_open_tract_area_threshold - other_than_tongue_tip).max())
    return max(worst_violations) / other_open_tract_area_threshold


def tongue_body_closure(seq: Sequence,
                        tongue_tip_length,
                        idx_slice=None,
                        unclosed_tract_area_threshold=DEFAULT_UNCLOSED_TRACT_AREA_THRESHOLD,
                        maximum_tract_area=DEFAULT_MAX_TRACT_AREA,
                        **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    tongue_idx = pd.IndexSlice[:, "tongue"]
    violations = []
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        tongue_from_tip_to_body = tubes.loc[tongue_idx, :].iloc[::-1]
        tongue_positions_relative_to_tip = np.cumsum(tongue_from_tip_to_body["tube_length"])
        tongue_body = tongue_from_tip_to_body.loc[tongue_positions_relative_to_tip >= tongue_tip_length]["tube_area"]
        tongue_body_violation = (tongue_body - vtl.TUBE_AREA_THRESHOLD).min() / maximum_tract_area
        if tongue_body_violation > 0.0 or unclosed_tract_area_threshold is None:
            violations.append(tongue_body_violation)
        else:
            other_than_tongue_body = tubes.loc[tubes.index.difference(tongue_body.index)]["tube_area"]
            other_worst_violation = (unclosed_tract_area_threshold - other_than_tongue_body).max() / unclosed_tract_area_threshold
            violations.append(other_worst_violation)
    return max(violations)


def other_than_tongue_body_open(seq: Sequence,
                                tongue_tip_length,
                                idx_slice=None,
                                other_open_tract_area_threshold=DEFAULT_UNCLOSED_TRACT_AREA_THRESHOLD,
                                **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    tongue_idx = pd.IndexSlice[:, "tongue"]
    worst_violations = []
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        tongue_from_tip_to_body = tubes.loc[tongue_idx, :].iloc[::-1]
        tongue_positions_relative_to_tip = np.cumsum(tongue_from_tip_to_body["tube_length"])
        tongue_body = tongue_from_tip_to_body.loc[tongue_positions_relative_to_tip >= tongue_tip_length]["tube_area"]
        other_than_tongue_body = tubes.loc[tubes.index.difference(tongue_body.index)]["tube_area"]
        worst_violations.append((other_open_tract_area_threshold - other_than_tongue_body).max())
    return max(worst_violations) / other_open_tract_area_threshold


def lip_closure(seq: Sequence,
                idx_slice=None,
                unclosed_tract_area_threshold=DEFAULT_UNCLOSED_TRACT_AREA_THRESHOLD,
                maximum_tract_area=DEFAULT_MAX_TRACT_AREA,
                **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    lower_lip_idx = pd.IndexSlice[:, "lower_lip"]
    violations = []
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        try:
            lower_lip = tubes.loc[lower_lip_idx, :]["tube_area"]
        except KeyError:
            violations.append(1.0)
        else:
            lower_lip_violation = (lower_lip - vtl.TUBE_AREA_THRESHOLD).min() / maximum_tract_area
            if lower_lip_violation > 0.0 or unclosed_tract_area_threshold is None:
                violations.append(lower_lip_violation)
            else:
                other_than_lower_lip = tubes.loc[tubes.index.difference(lower_lip.index)]["tube_area"]
                other_worst_violation = (unclosed_tract_area_threshold - other_than_lower_lip).max() / unclosed_tract_area_threshold
                violations.append(other_worst_violation)
    return max(violations)


def other_than_lip_open(seq: Sequence,
                        idx_slice=None,
                        other_open_tract_area_threshold=DEFAULT_UNCLOSED_TRACT_AREA_THRESHOLD,
                        **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    lower_lip_idx = pd.IndexSlice[:, "lower_lip"]
    worst_violations = []
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        try:
            lower_lip = tubes.loc[lower_lip_idx, :]["tube_area"]
        except KeyError:
            other_than_lower_lip = tubes.loc[:]["tube_area"]
        else:
            other_than_lower_lip = tubes.loc[tubes.index.difference(lower_lip.index)]["tube_area"]
        worst_violations.append((other_open_tract_area_threshold - other_than_lower_lip).max())
    return max(worst_violations) / other_open_tract_area_threshold


def mouth_open(seq: Sequence,
               idx_slice=None,
               mouth_open_tract_area_threshold=0.3,
               **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    mouth_idx = pd.IndexSlice[:, ["lower_incisors", "lower_lip"]]
    worst_violations = []
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        try:
            mouth = tubes.loc[mouth_idx, :]["tube_area"]
        except KeyError:
            worst_violations.append(1.0)
        else:
            worst_violations.append((mouth_open_tract_area_threshold - mouth).max())
    return max(worst_violations) / mouth_open_tract_area_threshold


def any_closure(seq: Sequence,
                idx_slice=None,
                maximum_tract_area=DEFAULT_MAX_TRACT_AREA,
                **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    violations = []
    for i in range(len(_seq)):
        tube_areas = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes["tube_area"]
        violation = (tube_areas - vtl.TUBE_AREA_THRESHOLD).min() / maximum_tract_area
        violations.append(violation)
    return max(violations)


def _articulator_closures(tubes, unclosed_area_threshold):
    closures = []
    for art in set(tubes.index.get_level_values("articulator")):
        art_tube_areas = tubes.loc[pd.IndexSlice[:, art], :]["tube_area"]
        if (art_tube_areas < unclosed_area_threshold).any():
            closures.append(art)
    return closures

def _contiguous_closure_lengths(tubes, unclosed_area_threshold):
    closed = []
    for i in range(len(tubes)):
        if tubes["tube_area"].iloc[i] < unclosed_area_threshold:
            closed.append(True)
        else:
            closed.append(False)
    closed_lengths = []
    i = 0
    for is_closed, run in groupby(closed):
        run = list(run)
        if is_closed:
           closed_lengths.append(tubes["tube_length"][i:i+len(run)].sum())
        i += len(run)
    return closed_lengths

##DEPRECATED:
def any_single_articulator_single_place_closure(seq: Sequence,
                                                idx_slice=None,
                                                single_place_closure_max_length=DEFAULT_SINGLE_PLACE_CLOSURE_MAX_LENGTH,
                                                minimum_open_area=0.1,
                                                basically_closed_area=0.1,
                                                **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        #full closure made!
        if not (tubes["tube_area"] < vtl.TUBE_AREA_THRESHOLD).any():
            return 1.0
        #other articulators mostly open
        art_closures = _articulator_closures(tubes, minimum_open_area)
        if len(art_closures) != 1:
            return 1.0
        #closure only made in one place
        art = art_closures[0]
        closure_lengths = _contiguous_closure_lengths(tubes.loc[pd.IndexSlice[:, art], :], basically_closed_area)
        if len(closure_lengths) != 1:
            return 1.0
        if closure_lengths[0] > single_place_closure_max_length:
            return 1.0
    return -1.0


def precise_closures(seq: Sequence,
                     idx_slice=None,
                     maximum_closure_length=DEFAULT_SINGLE_PLACE_CLOSURE_MAX_LENGTH,
                     basically_closed_area=0.1,
                     maximum_tract_length=DEFAULT_MAX_TRACT_LENGTH,
                     **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    worst_violations = []
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        closure_lengths = np.array(_contiguous_closure_lengths(tubes, basically_closed_area))
        try:
            worst_violation = (closure_lengths - maximum_closure_length).max() / maximum_tract_length
        except ValueError:
            # When there are no closures len(closure_lengths) == 0 and .max() will fail
            worst_violation = 1.0
        worst_violations.append(worst_violation)
    return max(worst_violations) 


def single_closure(seq: Sequence,
                   idx_slice=None,
                   basically_closed_area=0.3,
                   **kwargs) -> float:
    _seq = _apply_index_slice(seq, idx_slice)
    for i in range(len(_seq)):
        tubes = vtl.tube(_seq.iloc[i][list(VOCALTRACT_PARAMS)]).tubes
        closure_lengths = _contiguous_closure_lengths(tubes, basically_closed_area)
        if len(closure_lengths) > 1:
            return 1.0
    return -1.0


def achieved_targets(trj: Sequence,
                     tgt: Sequence,
                     tols: pd.Series,
                     seglabs=None,
                     params=None,
                     **kwargs) -> float:
    if params is None or params == "all":
        cols = list(VOCALTRACT_PARAMS + GLOTTIS_PARAMS)
    elif params == "vt":
        cols = list(VOCALTRACT_PARAMS)
    elif params == "gl":
        cols = list(GLOTTIS_PARAMS)
    else:
        cols = list(params)
    segs = (list(tgt.index.get_level_values(Sequence.IDX_NAMES[1]))
            if seglabs is None
            else seglabs)
    for seg in segs:
        trj_seg_fin = trj.loc[pd.IndexSlice[:, seg], cols].iloc[-1]
        tgt_seg = tgt.loc[pd.IndexSlice[:, seg], cols].iloc[0]
        within_tols = ((tgt_seg - trj_seg_fin).abs() < tols[cols]).all()
        if not within_tols:
            return 1.0
    return -1.0

##DEMIT -- GENERATE THESE ONES:
def vowel_tract_open(*args, **kwargs) -> float:
    return tract_open(*args, **kwargs, idx_slice=pd.IndexSlice[:, "V"])

def vowel_voiced(*args, **kwargs) -> float:
    return voiced(*args, **kwargs, idx_slice=pd.IndexSlice[:, "V"])

##
def consonant_tongue_tip_closure(*args, **kwargs) -> float:
    return tongue_tip_closure(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_other_than_tongue_tip_open(*args, **kwargs) -> float:
    return other_than_tongue_tip_open(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_tongue_body_closure(*args, **kwargs) -> float:
    return tongue_body_closure(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_other_than_tongue_body_open(*args, **kwargs) -> float:
    return other_than_tongue_body_open(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_lip_closure(*args, **kwargs) -> float:
    return lip_closure(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_other_than_lip_open(*args, **kwargs) -> float:
    return other_than_lip_open(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_mouth_open(*args, **kwargs) -> float:
    return mouth_open(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])
##

def consonant_lower_incisors_closure(*args, **kwargs) -> float:
    return lower_incisors_closure(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_any_closure(*args, **kwargs) -> float:
    return any_closure(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_any_single_articulator_single_place_closure(*args, **kwargs) -> float:
    return any_single_articulator_single_place_closure(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_precise_closures(*args, **kwargs) -> float:
    return precise_closures(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])

def consonant_single_closure(*args, **kwargs) -> float:
    return single_closure(*args, **kwargs, idx_slice=pd.IndexSlice[:, "C"])
