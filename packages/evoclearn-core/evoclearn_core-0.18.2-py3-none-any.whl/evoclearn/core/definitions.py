# -*- coding: utf-8 -*-


QTA_SLOPE_PREFIX = "d"
QTA_SLOPE = "slope"
QTA_VALUE = "val"
QTA_TIME_CONSTANT = "tau_s"
QTA_DURATION = "duration_s"

VOCALTRACT_PARAMS = (
    "HX",       # Horz. Hyoid pos.
    "HY",       # Vert. Hyoid pos.
    "JX",       # Horz. Jaw pos.
    "JA",       # Jaw angle (deg.)
    "LP",       # Lip protrusion
    "LD",       # Lip distance
    "VS",       # Velum shape
    "VO",       # Velic opening
    "TCX",      # Tongue body X
    "TCY",      # Tongue body Y
    "TTX",      # Tongue tip X
    "TTY",      # Tongue tip Y
    "TBX",      # Tongue blade X
    "TBY",      # Tongue blade Y
    "TRX",      # Tongue root X
    "TRY",      # Tongue root Y
    "TS1",      # Tongue side elev. 1
    "TS2",      # Tongue side elev. 2 (back region)
    "TS3"       # Tongue side elev. 3 (tip region)
    )

GLOTTIS_PARAMS = (
    "_F0",      # Fundamental frequency
    "_SP",      # Subglottal pressure
    "_LD",      # Lower rest displacement
    "_UD",      # Upper rest displacement
    "_CA",      # Chink area
    "_PL",      # Phase lag
    "_RA",      # Relative amplitude
    "_DP",      # Double pulsing
    "_PS",      # Pulse skewness
    "_FL",      # Flutter
    "_AS"       # Aspiration strength
    )

VOCALTRACTLAB_PARAMS = (
    VOCALTRACT_PARAMS +
    GLOTTIS_PARAMS
    )

TARGETS_TIMECONSTANTS_PARAMS = (
    VOCALTRACT_PARAMS +
    ("vt_" + QTA_TIME_CONSTANT,) +  # Vocal tract param. time constant (qTA)
    GLOTTIS_PARAMS +
    ("gl_" + QTA_TIME_CONSTANT,)    # Glottal param. time constant (qTA)
    )

QTA_COMPLETE_PARAMS = (
    TARGETS_TIMECONSTANTS_PARAMS +
    tuple(QTA_SLOPE_PREFIX + param for param in VOCALTRACT_PARAMS) +
    tuple(QTA_SLOPE_PREFIX + param for param in GLOTTIS_PARAMS) +
    (QTA_DURATION,)
    )

DEFAULT_VARIABLE_PARAMS = frozenset([
    "HX", "HY", "JX", "JA", "LP", "LD", "VS", "VO",
    "TCX", "TCY", "TTX", "TTY", "TBX", "TBY", "TRX", "TRY",
    "vt_tau_s", "gl_tau_s"
    ])

CONSONANT_CONTROL_PARAMS = {
    "bilabial_stop": ("JX", "JA",
                      "LD",
                      "vt_tau_s", "gl_tau_s"),
    "alveolar_stop": ("JX", "JA",
                      "TTX", "TTY", "TBX", "TBY",
                      "vt_tau_s", "gl_tau_s"),
    "velar_stop": ("JX", "JA",
                   "TCY",
                   "vt_tau_s", "gl_tau_s")
    }

# X-SAMPA
CONSONANT_TYPE_MAP = {
    "b": "bilabial_stop",
    "d": "alveolar_stop",
    "g": "velar_stop"
    }
