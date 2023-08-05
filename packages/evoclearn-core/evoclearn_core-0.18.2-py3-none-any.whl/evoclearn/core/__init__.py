# -*- coding: utf-8 -*-

from collections import namedtuple

from .version import __version__
from .definitions import *
from .sequence import Sequence, Sequences
from .track import Track, Tracks

Waveform = namedtuple("Waveform", ["samples", "samplerate"])
