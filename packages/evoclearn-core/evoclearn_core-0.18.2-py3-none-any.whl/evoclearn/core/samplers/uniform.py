# -*- coding: utf-8 -*-

from typing import Iterable
import itertools

import pandas as pd
import numpy as np

from .. import Sequence, Sequences
from ..utils import standard_param_order


class Uniform(object):
    def __init__(self, bounds: dict, labels: list=None, seed: int=None):
        """
        :param bounds: Parameter limits
        :param labels: Segment (row index) labels (also determines how many)
        :param seed: The random number generator seed
        """
        self.bounds = pd.DataFrame(bounds, columns=standard_param_order(bounds))
        self.labels = labels if labels is not None else ["_"]
        self.seed = seed
        self.random_state = np.random.RandomState(self.seed)

    def __iter__(self) -> Iterable[Sequence]:
        return self

    def __next__(self) -> Sequence:
        num_segs = len(self.labels)
        num_params = len(self.bounds.columns)
        ar = self.random_state.random_sample((num_segs, num_params))
        mi = pd.MultiIndex.from_tuples(enumerate(self.labels),
                                       names=Sequence.IDX_NAMES)
        df = pd.DataFrame(ar, columns=self.bounds.columns, index=mi)
        mins = self.bounds.loc["min"]
        ranges = self.bounds.loc["max"] - mins
        return Sequence((df * ranges) + mins)

    def sequences(self, num_seqs: int) -> Sequences:
        num_segs = len(self.labels)
        num_params = len(self.bounds.columns)
        ar = self.random_state.random_sample((num_segs * num_seqs, num_params))
        mi = ((sample, segindex, seglabel)
              for sample, (segindex, seglabel)
              in itertools.product(range(num_seqs),
                                   enumerate(self.labels)))
        mi = pd.MultiIndex.from_tuples(mi, names=Sequences.IDX_NAMES)
        df = pd.DataFrame(ar, index=mi, columns=self.bounds.columns)
        mins = self.bounds.loc["min"]
        ranges = self.bounds.loc["max"] - mins
        return Sequences((df * ranges) + mins)
    
