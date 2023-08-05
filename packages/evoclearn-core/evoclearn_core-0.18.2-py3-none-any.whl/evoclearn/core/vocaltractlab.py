# -*- coding: utf-8 -*-

import os
import ctypes
import platform
from collections import namedtuple

import pandas as pd
import numpy as np

from . import Sequence, VOCALTRACT_PARAMS, GLOTTIS_PARAMS
from . import log


LOGGER = log.getLogger("evl.core.vocaltractlab")
LIB = None
NUM_TUBE_SECTIONS = None
FRAMESAMPLES = 110
AUDIO_SAMPLERATE = 44100
TUBE_AREA_THRESHOLD = 0.0002  # min. seems to be: 0.0001

TUBE_ARTICULATORS = {0: "vocal_folds",
                     1: "tongue",
                     2: "lower_incisors",
                     3: "lower_lip",
                     4: "other"}

Tube = namedtuple("Tube",
                  ["tubes",
                   "incisor_position",
                   "tonguetip_side_elevation",
                   "velum_opening"])

def initialise(speakerfilename: str) -> ctypes.CDLL:
    global LIB
    global NUM_TUBE_SECTIONS
    if LIB is not None:
        LOGGER.warning("It is only possible to have a single "
                       "instance of the VTL API per OS process. "
                       "THIS CALL WILL RECONFIGURE THE LIB FOR THE "
                       "ENTIRE PROCESS...")
    if platform.system() == "Windows":
        so_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "VocalTractLabApi.dll")
        LIB = ctypes.windll.LoadLibrary(so_path)
    else:
        so_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "VocalTractLabApi.so")
        LIB = ctypes.cdll.LoadLibrary(so_path)
    # Loading speaker file is necessary for extracting the constants and the
    # vtlInitialize function needs to be called before calling other VTL API
    # functions
    speaker_file_name = ctypes.c_char_p(speakerfilename.encode())
    LIB.vtlInitialize(speaker_file_name)
    # Get constants from VTL
    audio_sampling_rate = ctypes.c_int(0)
    number_tube_sections = ctypes.c_int(0)
    number_vocal_tract_parameters = ctypes.c_int(0)
    number_glottis_parameters = ctypes.c_int(0)
    LIB.vtlGetConstants(ctypes.byref(audio_sampling_rate),
                        ctypes.byref(number_tube_sections),
                        ctypes.byref(number_vocal_tract_parameters),
                        ctypes.byref(number_glottis_parameters))
    NUM_TUBE_SECTIONS = number_tube_sections.value
    # Check that core API settings align with evl_core definitions
    assert audio_sampling_rate.value == AUDIO_SAMPLERATE
    assert number_vocal_tract_parameters.value == len(VOCALTRACT_PARAMS)
    assert number_glottis_parameters.value == len(GLOTTIS_PARAMS)
    return LIB


def synthesise(param_curves: Sequence,
               framesamples: int=FRAMESAMPLES) -> np.ndarray:
    if LIB is None:
        raise RuntimeError("Need to call vocaltractlab.initialise() first...")
    num_frames = len(param_curves)
    num_samples = int((num_frames - 1) * framesamples)
    # Create C arrays and copy param curve values from input
    a = param_curves[list(VOCALTRACT_PARAMS)].to_numpy()
    vocaltract_params = a.ravel("C")
    vtl_tract_params = (ctypes.c_double * len(vocaltract_params))()
    vtl_tract_params[:] = vocaltract_params
    glottis_params = param_curves[list(GLOTTIS_PARAMS)].to_numpy().ravel("C")
    vtl_glott_params = (ctypes.c_double * len(glottis_params))()
    vtl_glott_params[:] = glottis_params
    # Create other references for API call
    vtl_audio = (ctypes.c_double * num_samples)()
    vtl_enable_console_output = ctypes.c_int(0)
    vtl_num_frames = ctypes.c_int(num_frames)
    vtl_framesamples = ctypes.c_int(framesamples)
    # Synth block and return
    errcode = LIB.vtlSynthBlock(ctypes.byref(vtl_tract_params),    # input
                                ctypes.byref(vtl_glott_params),    # input
                                vtl_num_frames,                    # input
                                vtl_framesamples,                  # input
                                ctypes.byref(vtl_audio),           # output
                                vtl_enable_console_output)         # input
    if errcode != 0:
        raise RuntimeError(f"Error in vtlSynthBlock! Errorcode: {errcode}")
    arr = np.array(vtl_audio)
    return arr


def synthesise2(param_curves: Sequence,
                framesamples: int=FRAMESAMPLES) -> np.ndarray:
    if LIB is None:
        raise RuntimeError("Need to call vocaltractlab.initialise() first...")
    num_frames = len(param_curves)
    num_samples = int((num_frames - 1) * framesamples)
    vtl_audio = (ctypes.c_double * num_samples)()

    LIB.vtlSynthesisReset()

    for i in range(num_frames):
        #First call to "vtlSynthesisAddTract" will not synthesise audio:
        vtl_new_samples = ctypes.c_int(0) if i == 0 else ctypes.c_int(framesamples)
        audio_offset = (0 if i == 0 else i - 1) * framesamples
        #
        current_frame = param_curves.iloc[i]
        vtl_tract_params = (ctypes.c_double * len(VOCALTRACT_PARAMS))()
        vtl_tract_params[:] = current_frame[list(VOCALTRACT_PARAMS)]
        vtl_glott_params = (ctypes.c_double * len(GLOTTIS_PARAMS))()
        vtl_glott_params[:] = current_frame[list(GLOTTIS_PARAMS)]

        LIB.vtlSynthesisAddTract(vtl_new_samples,                 #input
                                 ctypes.byref(vtl_audio,          #output
                                              ctypes.sizeof(ctypes.c_double) * audio_offset),
                                 ctypes.byref(vtl_tract_params),  #input
                                 ctypes.byref(vtl_glott_params))  #input
    arr = np.array(vtl_audio)
    return arr


def transfer_function(frame, n_spectrum_samples: int=2048) -> (np.ndarray, np.ndarray):
    if LIB is None:
        raise RuntimeError("Need to call vocaltractlab.initialise() first...")
    df = frame[list(VOCALTRACT_PARAMS)]
    n_vtps = len(VOCALTRACT_PARAMS)
    vtps_ctype = ctypes.c_double * n_vtps
    vtps = vtps_ctype()
    vtps[:] = df.values.flatten()
    #
    spectrum_ctype = ctypes.c_double * n_spectrum_samples
    magnitude_spectrum = spectrum_ctype()
    phase_spectrum = spectrum_ctype()  # in radians
    LIB.vtlGetTransferFunction(ctypes.byref(vtps),  # input
                               n_spectrum_samples,  # input
                               ctypes.byref(magnitude_spectrum),  # output
                               ctypes.byref(phase_spectrum))      # output
    return np.array(magnitude_spectrum), np.array(phase_spectrum)


def tube(frame) -> (pd.DataFrame, float, float, float):
    if LIB is None:
        raise RuntimeError("Need to call vocaltractlab.initialise() first...")
    df = frame[list(VOCALTRACT_PARAMS)]
    n_vtps = len(VOCALTRACT_PARAMS)
    vtps_ctype = ctypes.c_double * n_vtps
    vtps = vtps_ctype()
    vtps[:] = df.values.flatten()
    #
    double_array_ctype = ctypes.c_double * NUM_TUBE_SECTIONS
    int_array_ctype = ctypes.c_int * NUM_TUBE_SECTIONS
    tube_length = double_array_ctype()
    tube_area = double_array_ctype()
    tube_articulator = int_array_ctype()
    incisor_position = ctypes.c_double(0.0)
    tonguetip_side_elevation = ctypes.c_double(0.0)
    velum_opening = ctypes.c_double(0.0)
    LIB.vtlTractToTube(ctypes.byref(vtps),                     # input
                       ctypes.byref(tube_length),              # output
                       ctypes.byref(tube_area),                # output
                       ctypes.byref(tube_articulator),         # output
                       ctypes.byref(incisor_position),         # output
                       ctypes.byref(tonguetip_side_elevation), # output
                       ctypes.byref(velum_opening))            # output
    # Create tubes dataframe:
    tube_articulators = np.array(tube_articulator, dtype=int)
    mi = pd.MultiIndex.from_tuples(enumerate([TUBE_ARTICULATORS[a]
                                              for a in tube_articulators]),
                                   names=["idx", "articulator"])

    tubes = pd.DataFrame(list(zip(tube_length, tube_area)),
                         index=mi,
                         columns=["tube_length", "tube_area"],
                         dtype=np.float)
    return Tube(tubes,
                float(incisor_position.value),
                float(tonguetip_side_elevation.value),
                float(velum_opening.value))


def tract_to_svg_file(frame: pd.DataFrame, fname: str):
    if LIB is None:
        raise RuntimeError("Need to call vocaltractlab.initialise() first...")
    df = frame[list(VOCALTRACT_PARAMS)]
    n_vtps = len(VOCALTRACT_PARAMS)
    vtps_ctype = ctypes.c_double * n_vtps
    vtps = vtps_ctype()
    vtps[:] = df.values.flatten()
    e = LIB.vtlExportTractSvg(ctypes.byref(vtps), fname.encode())
    if e != 0:
        raise Exception(f"Error from VocalTractLabApi (error={e})")
