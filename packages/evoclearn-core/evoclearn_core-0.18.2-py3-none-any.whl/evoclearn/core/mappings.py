# -*- coding: utf-8 -*-
""" Functions that map a single Sequence or object to a new Sequence or object
(one-to-one) """

from typing import Iterable, Callable, Optional

import pandas as pd
import numpy as np
import librosa

from . import Sequence, Track, Waveform
from . import utils
from . import qta
from . import features
from . import distance
from . import definitions as defs
from . import vocaltractlab as vtl
from . import log
from .constraints import simple_constraints


LOGGER = log.getLogger("evl.core.mappings")


def satisfies_constraints(
    seq: Sequence,
    constraints: Iterable[Callable[[Sequence], bool]]=simple_constraints
    ) -> bool:
    return all(f(seq) for f in constraints)


def normalise_minmax(seq: pd.DataFrame,
                     bounds: dict,
                     lb: float=-1.0,
                     ub: float=1.0,
                     inverse: bool=False) -> pd.DataFrame:
    bounds = pd.DataFrame(bounds)[seq.columns]
    return utils.normalise_minmax(seq, bounds, lb, ub, inverse)


def normalise_standard(seq: pd.DataFrame,
                       stats: dict,
                       inverse: bool=False) -> pd.DataFrame:
    stats = pd.DataFrame(stats)[seq.columns]
    return utils.normalise_standard(seq, stats, inverse)


def add_slope_and_duration(seq: Sequence,
                           durations: Iterable[float]) -> Sequence:
    """All targets and time constants need to be supplied in the input
    target sequence, slopes are optional, if not specified these will
    default to 0.0"""
    input_cols = set(seq.columns)
    complete_target_cols = defs.TARGETS_TIMECONSTANTS_PARAMS
    is_complete = (input_cols.intersection(complete_target_cols) ==
                   set(complete_target_cols))
    assert is_complete, "Need all target parameters for complete qTA sequence"
    df = pd.DataFrame(np.nan, index=seq.index, columns=defs.QTA_COMPLETE_PARAMS)
    df[seq.columns] = seq[seq.columns]
    df[defs.QTA_DURATION] = durations
    df.fillna(0.0, inplace=True)
    return Sequence(df)


def target_approximation(seq: Sequence,
                         vtl_framesamples: int=vtl.FRAMESAMPLES,
                         vtl_audiosamplerate: int=vtl.AUDIO_SAMPLERATE,
                         fadein_subglottal_pressure=True) -> Sequence:
    # Construct the dataframe for the trajectories
    frames_total = int(seq[defs.QTA_DURATION].sum() * vtl_audiosamplerate) // vtl_framesamples + 1
    frames_per_target = utils.weights_to_ints(seq[defs.QTA_DURATION], frames_total)
    target_labels = seq.index.get_level_values(Sequence.IDX_NAMES[-1])
    labels = []
    for nframes, label in zip(frames_per_target, target_labels):
        labels += [label] * nframes
    mi = pd.MultiIndex.from_tuples(enumerate(labels),
                                   names=Sequence.IDX_NAMES)
    param_curves = pd.DataFrame(np.nan, index=mi, columns=defs.VOCALTRACTLAB_PARAMS)
    # Select and calculate trajectory for each param using target approximation
    for paramlist, prefix in zip([defs.VOCALTRACT_PARAMS, defs.GLOTTIS_PARAMS],
                                 ["vt_", "gl_"]):
        for param in paramlist:
            qta_params = pd.DataFrame(seq[[param,
                                           defs.QTA_SLOPE_PREFIX + param,
                                           prefix + defs.QTA_TIME_CONSTANT,
                                           defs.QTA_DURATION]].to_numpy(),
                                      columns=[defs.QTA_VALUE,
                                               defs.QTA_SLOPE,
                                               defs.QTA_TIME_CONSTANT,
                                               defs.QTA_DURATION])
            param_curves[param] = qta.target_approximation(qta_params,
                                                           vtl_framesamples)
    if fadein_subglottal_pressure:
        param_curves.iloc[0, param_curves.columns.get_loc("_SP")] = 0.0
        param_curves.iloc[1, param_curves.columns.get_loc("_SP")] = param_curves.iloc[2, param_curves.columns.get_loc("_SP")] / 2.0
    return Sequence(param_curves)


def vtl_curves_from_targets(seq: Sequence,
                            durations: Iterable[float],
                            vtl_framesamples: int=vtl.FRAMESAMPLES) -> Sequence:
    complete_qta_targets = add_slope_and_duration(seq, durations)
    vtl_curves = target_approximation(complete_qta_targets, vtl_framesamples)
    return vtl_curves


def synthesise_vtl_curves(seq: Sequence,
                          vtl_framesamples: int=vtl.FRAMESAMPLES) -> np.ndarray:
    return vtl.synthesise(seq, vtl_framesamples)

def synthesise_vtl_curves2(seq: Sequence,
                           vtl_framesamples: int=vtl.FRAMESAMPLES) -> Waveform:
    return Waveform(samples=vtl.synthesise(seq, vtl_framesamples),
                    samplerate=vtl.AUDIO_SAMPLERATE)

def linear_fade(audio: np.ndarray,
                samplerate: int=vtl.AUDIO_SAMPLERATE,
                in_seconds: float=0.005,
                out_seconds: float=0.005) -> np.ndarray:
    a = audio.copy()
    #fade in:
    n = int(samplerate * in_seconds)
    a[:n] = a[:n] * np.linspace(0.0, 1.0, n)
    #fade out:
    n = int(samplerate * out_seconds)
    a[-n:] = a[-n:] * np.linspace(1.0, 0.0, n)
    return a


def get_features(audio: np.ndarray,
                 audio_samplerate=vtl.AUDIO_SAMPLERATE,
                 fade_in_out: Optional[float]=0.005,
                 **kwargs) -> np.ndarray:
    """See core.features.get_features for descriptions of **kwargs"""
    if fade_in_out is not None:
        audio = (linear_fade(audio,
                             samplerate=audio_samplerate,
                             in_seconds=fade_in_out,
                             out_seconds=fade_in_out)
                 if fade_in_out
                 else audio)
    return features.get_features(audio,
                                 sr_in=audio_samplerate,
                                 **kwargs)[0].T


def get_error(feat: np.ndarray, ref_feat: np.ndarray, **kwargs) -> float:
    if len(ref_feat) < len(feat):
        raise ValueError("Ref feats should not be shorter than synth...")
    lendiff = len(ref_feat) - len(feat)
    if lendiff > 3:
        raise ValueError("Ref feats much longer than synth"
                         f" ({len(ref_feat)} vs {len(feat)})")
    if lendiff:
        #Pad feat frames by repeating the last few...
        repeat_frames = feat[-lendiff:]
        feat = np.concatenate((feat, repeat_frames))
    return float(features.get_error(feat.T, ref_feat.T, **kwargs))


def feattrack(audio: np.ndarray,
              audio_samplerate=vtl.AUDIO_SAMPLERATE,
              fade_in_out: Optional[float]=0.005,
              center_frame=True,
              pad_mode="symmetric",
              win_func="hamming",
              win_length_s=features.ASR_FEATS["win_length_s"],
              hop_length_s=features.ASR_FEATS["hop_length_s"],
              **kwargs) -> Track:
    """See core.features.get_features for descriptions of **kwargs"""
    if "roi" in kwargs:
        raise ValueError("Not accepting ROI here, slice input or output as needed...")
    if fade_in_out is not None:
        audio = (linear_fade(audio,
                             samplerate=audio_samplerate,
                             in_seconds=fade_in_out,
                             out_seconds=fade_in_out)
                 if fade_in_out
                 else audio)
    featarray = features.get_features(audio,
                                      sr_in=audio_samplerate,
                                      center_frame=center_frame,
                                      pad_mode=pad_mode,
                                      win_func=win_func,
                                      win_length_s=win_length_s,
                                      hop_length_s=hop_length_s,
                                      **kwargs)[0].T
    if center_frame:
        times = np.arange(len(featarray)) * hop_length_s
    else:
        times = np.arange(len(featarray)) * hop_length_s + (win_length_s / 2.0)
    return Track(featarray, index=times)

def feattrack2(waveform: Waveform, **kwargs):
    if "audio_samplerate" in kwargs:
        raise Exception("feattrack2() does not support audio_samplerate argument...")
    return feattrack(audio=waveform.samples,
                     audio_samplerate=waveform.samplerate,
                     **kwargs)

def resample_wave(waveform: Waveform, samplerate) -> Waveform:
    if waveform.samplerate == samplerate:
        return waveform
    # LOGGER.debug("resample_wav(): %s -> %s", waveform.samplerate, samplerate)
    a = librosa.resample(waveform.samples,
                         orig_sr=waveform.samplerate,
                         target_sr=samplerate)
    return Waveform(samples=a, samplerate=samplerate)

def mfccs(audio: np.ndarray,
          audio_samplerate=vtl.AUDIO_SAMPLERATE,
          fade_in_out: Optional[float]=0.005,
          delta=True,
          accel=True,
          c0=True,
          winlen=features.EST_MFCC["winlen"],
          winstep=features.EST_MFCC["winstep"],
          **kwargs) -> Track:
    if "roi" in kwargs:
        raise ValueError("Not accepting ROI here, slice input or output as needed...")
    if fade_in_out is not None:
        audio = (linear_fade(audio,
                             samplerate=audio_samplerate,
                             in_seconds=fade_in_out,
                             out_seconds=fade_in_out)
                 if fade_in_out
                 else audio)
    mfcc_array = features.get_mfccs(audio,
                                    sr=audio_samplerate,
                                    delta=delta,
                                    accel=accel,
                                    c0=c0,
                                    winlen=winlen,
                                    winstep=winstep,
                                    **kwargs)
    times = np.arange(len(mfcc_array)) * winstep + (winlen / 2.0)
    return Track(mfcc_array, index=times)


def dist_fbf(sample: Track, reference: Track, **kwargs) -> Track:
    """The time instants of the `reference` will be preserved in the
    output track"""
    return Track(distance.frame_by_frame(sample.to_numpy(),
                                         reference.to_numpy(),
                                         **kwargs),
                 index=reference.index)


def dist_dtw(sample: Track, reference: Track, **kwargs) -> Track:
    """The time instants corresponding to the `reference` will be
    represented in the output track"""
    d, sample_i, reference_i = distance.dtw(sample.to_numpy(),
                                            reference.to_numpy(),
                                            **kwargs)
    return Track(d, index=reference.index[reference_i])


def objective(sample: Track,
              reference: Track,
              rois=None,
              distf=dist_fbf,
              aggf=lambda x: np.mean(np.square(x)),
              max_frames_diff=3,
              pad_sample=False,
              **distf_kwargs) -> float:
    frames_diff = len(reference) - len(sample)
    if max_frames_diff is not None:
        if len(sample) > len(reference):
            raise ValueError("Reference track should not be shorter than sample")
        if frames_diff > max_frames_diff:
            raise ValueError("Reference track much longer than sample "
                             f"({len(reference)} >> {len(sample)})")
    if pad_sample and frames_diff > 0:
        sample = Track.pad(sample, len(reference), location="back")
    d = distf(sample, reference, **distf_kwargs)
    return (float(aggf(d.to_numpy()))
            if rois is None
            else float(aggf(d.slice_ranges(rois).to_numpy())))


def scan_vtln_warp_factor(audio: np.ndarray,
                          ref_audio: np.ndarray,
                          warpfactor_start: float=0.1,
                          warpfactor_end: float=1.8,
                          warpfactor_step: float=0.01,
                          warpfunction: str="symmetric",
                          audio_samplerate: int=vtl.AUDIO_SAMPLERATE,
                          fade_in_out: Optional[float]=0.005,
                          winlen_s: float=0.010) -> float:
    """Samplerate needs to match audio_samplerate for both inputs"""
    # Downsample to librosa standard and check lengths match approximately:
    sr = 22050
    if audio_samplerate != sr:
        audio = librosa.resample(audio,
                                 orig_sr=audio_samplerate,
                                 target_sr=sr)
        ref_audio = librosa.resample(ref_audio,
                                     orig_sr=audio_samplerate,
                                     target_sr=sr)
    lendiff = len(audio) - len(ref_audio)
    framesamplen = vtl.FRAMESAMPLES / vtl.AUDIO_SAMPLERATE * sr
    if abs(lendiff) > (framesamplen):
        raise ValueError(f"Audio lengths differ by more than a frame length... ({lendiff})")
    # Apply linear fade in/out to reduce edge effects in spectrum:
    if fade_in_out is not None:
        audio = (linear_fade(audio,
                             samplerate=sr,
                             in_seconds=fade_in_out,
                             out_seconds=fade_in_out)
                 if fade_in_out
                 else audio)
        ref_audio = (linear_fade(ref_audio,
                                 samplerate=sr,
                                 in_seconds=fade_in_out,
                                 out_seconds=fade_in_out)
                     if fade_in_out
                     else ref_audio)
    # Pad (back) for slight missmatches in lengths:
    if lendiff < 0:
        audio = np.pad(audio,
                       (0, abs(lendiff)),
                       mode="constant",
                       constant_values=0.0)
    if lendiff > 0:
        ref_audio = np.pad(ref_audio,
                           (0, abs(lendiff)),
                           mode="constant",
                           constant_values=0.0)
    # Do STFT and scan warping factors:
    winlen = int(sr * winlen_s)
    n_fft = int(2 ** np.ceil(np.log2(winlen)))
    spectrum = np.abs(librosa.stft(audio,
                                   window="hamming",
                                   center=True,
                                   n_fft=n_fft,
                                   win_length=winlen,
                                   hop_length=int(sr * 0.005),
                                   pad_mode="symmetric") ** 2).T
    ref_spectrum = np.abs(librosa.stft(ref_audio,
                                       window="hamming",
                                       center=True,
                                       n_fft=n_fft,
                                       win_length=winlen,
                                       hop_length=int(sr * 0.005),
                                       pad_mode="symmetric") ** 2).T
    warpfactor = utils.scan_vtln_warp_factor(spectrum,
                                             ref_spectrum,
                                             warpfactor_start,
                                             warpfactor_end,
                                             warpfunction,
                                             warpfactor_step)
    return float(warpfactor)
