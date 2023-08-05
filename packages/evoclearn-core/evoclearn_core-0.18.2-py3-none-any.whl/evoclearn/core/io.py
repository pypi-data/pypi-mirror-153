# -*- coding: utf-8 -*-

from typing import IO, Iterable, List, Tuple
import json
from xml.etree import ElementTree

import numpy as np
import pandas as pd
from scipy.io import wavfile
from praatio import textgrid as tgio
import librosa

from . import Sequence, Waveform
from . import definitions as defs
from . import vocaltractlab as vtl


def load_bounds_constraints(boundsfile: IO, params: Iterable[str]=None) -> Tuple[dict, dict]:
    speaker_bounds = json.load(boundsfile)
    bounds = speaker_bounds["vtl"]
    constraints = speaker_bounds["constraints"]
    if params is not None:
        bounds = {dim: bounds[dim] for dim in params}
    return bounds, constraints


def load_bounds(boundsfile: IO, params: Iterable[str]=None) -> dict:
    return load_bounds_constraints(boundsfile, params)[0]


def parammagnitudes_from_bounds(bounds: dict) -> pd.Series:
    df = pd.DataFrame(bounds)
    tol = df.loc["max"] - df.loc["min"]
    return tol


def default_sequence_from_bounds(bounds: dict, labels: list=None) -> Sequence:
    params = list(bounds)
    neutral_targets = [bounds[p]["default"] for p in params]
    seq = Sequence.from_spec(params, labels)
    seq.loc[:, params] = neutral_targets
    return seq


def read_durations_from_textgrid(path: str, tier: str, include_empty: bool=False) -> List[float]:
    """read duration array function
    """
    tg = tgio.openTextgrid(path, includeEmptyIntervals=include_empty)
    durations = [e.end - e.start for e in tg.tierDict[tier].entryList]
    return durations


def read_intervals_from_textgrid(path: str, tier: str, include_empty: bool=False) -> List[Tuple[float]]:
    tg = tgio.openTextgrid(path, includeEmptyIntervals=include_empty)
    intervals = [(e.start, e.end) for e in tg.tierDict[tier].entryList]
    return intervals


def float_to_int16(samples: np.ndarray) -> np.ndarray:
    a = np.int16(samples.astype(np.float64) * (2**15))
    np.clip(a, -2**15, 2**15-1, out=a)
    return a


def int16_to_float(samples: np.ndarray, dtypef=np.float32) -> np.ndarray:
    return dtypef(samples / (2**15))


def wav_float_to_int16(wav: Waveform) -> Waveform:
    if wav.samples.dtype == np.int16:
        return wav
    else:
        s = float_to_int16(wav.samples)
        return Waveform(s, wav.samplerate)

    
def wav_int16_to_float(wav: Waveform, dtypef=np.float32) -> Waveform:
    if wav.samples.dtype == np.int16:
        s = int16_to_float(wav.samples, dtypef)
        return Waveform(s, wav.samplerate)
    else:
        return wav

    
def wav_write(audio: np.ndarray,
              path: str,
              samplerate_hz=vtl.AUDIO_SAMPLERATE) -> None:
    """Writes signed 16-bit wav file from float audio array"""
    wavfile.write(path, samplerate_hz, float_to_int16(audio))


def load_audio(path: str, sr=None) -> Waveform:
    return Waveform(*librosa.load(path, sr=sr))


def load_vtl_curves(curvesfile: IO) -> Sequence:
    gl_params = []
    vt_params = []
    for line in curvesfile:
        if line.strip().startswith("#"):
            continue
        try:
            params = [float(field) for field in line.split()]
            if len(params) == len(defs.VOCALTRACT_PARAMS):
                vt_params.append(params)
            elif len(params) == len(defs.GLOTTIS_PARAMS):
                gl_params.append(params)
        except ValueError:
            pass
    if len(gl_params) != len(vt_params):
        raise Exception("len(gl_params) != len(vt_params)")
    # Construct the dataframe for the trajectories (TODO: pull next few lines
    # into separate func for reuse -- also needed in mappings.py):
    frames_total = len(gl_params)
    labels = ["UNK"] * frames_total
    mi = pd.MultiIndex.from_tuples(enumerate(labels),
                                   names=Sequence.IDX_NAMES)
    param_curves = pd.DataFrame(np.nan, index=mi, columns=defs.VOCALTRACTLAB_PARAMS)
    vt_params = np.array(vt_params)
    gl_params = np.array(gl_params)
    param_curves.loc[:,list(defs.VOCALTRACT_PARAMS)] = vt_params
    param_curves.loc[:,list(defs.GLOTTIS_PARAMS)] = gl_params
    return Sequence(param_curves)


class SpeakerFile(object):
    GLOTTIS_INDEX_MAP = {str(i): v for i, v in enumerate(defs.GLOTTIS_PARAMS)}

    def __init__(self, xmlpath):
        self._tree = ElementTree.parse(xmlpath)

    def vt_target(self, shape_name):
        shapes = self._tree.find("vocal_tract_model").find("shapes")
        for shape in shapes.findall("shape"):
            if shape.attrib["name"] == shape_name:
                params = []
                values = []
                for param in shape.findall("param"):
                    params.append(param.attrib["name"])
                    values.append(float(param.attrib["value"]))
                seq = Sequence.from_spec(params, fill_value=0.0)
                seq[params] = values
                return seq
        raise KeyError(f"Shape '{shape_name}' not defined in vocal tract model...")

    def gl_target(self, shape_name):
        glmodels = self._tree.find("glottis_models")
        for glmodel in glmodels.findall("glottis_model"):
            if glmodel.attrib["selected"] == "1":
                shapes = glmodel.find("shapes")
                for shape in shapes.findall("shape"):
                    if shape.attrib["name"] == shape_name:
                        params = []
                        values = []
                        for param in shape.findall("control_param"):
                            params.append(self.GLOTTIS_INDEX_MAP[param.attrib["index"]])
                            values.append(float(param.attrib["value"]))
                        seq = Sequence.from_spec(params, fill_value=0.0)
                        seq[params] = values
                        return seq
        raise KeyError(f"Shape '{shape_name}' not defined in selected glottis model...")
