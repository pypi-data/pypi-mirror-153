# -*- coding: utf-8 -*-

from typing import Iterable, List
import itertools

import pandas as pd
import numpy as np

from .. import Sequence, Sequences
from .. import definitions as defs
from ..utils import standard_param_order, consonant_control_params


class UniformProbLink(object):
    INDEPENDENT_PARAMS = ("HX", "HY", "JX", "JA",
                          "LP", "LD", "VS", "TBX", "TBY",
                          "vt_tau_s", "gl_tau_s")
    PROBLINK_PARAMS = ("TCX", "TCY", "TTX", "TTY", "VO")
    DERIVED_PARAMS = ("TRX", "TRY")
    DEFAULT_PARAMS = ("TS1", "TS2", "TS3",
                      "_F0", "_SP", "_LD", "_UD", "_CA", "_PL", "_RA", "_DP", "_PS", "_FL", "_AS")

    def __init__(self,
                 bounds: dict,
                 consonants: List[str]=None,
                 seed: int=None):
        """
        :param bounds: Parameter limits and defaults
        :param consonants: Specifies the consonants (determines control params)
        :param seed: The random number generator seed
        """
        if not all([p in bounds for p in defs.TARGETS_TIMECONSTANTS_PARAMS]):
            raise Exception("Need limits for all VTP parameters")
        self.bounds = pd.DataFrame(bounds,
                                   columns=standard_param_order(bounds))
        self.consonants = consonants or []
        self.seed = seed
        self.random_state = np.random.RandomState(self.seed)
        self._best_vtp_vparams = None

    @property
    def best_vowel_vocaltract_params(self):
        return self._best_vtp_vparams

    @best_vowel_vocaltract_params.setter
    def best_vowel_vocaltract_params(self, x):
        try:
            # First expect a pandas Series
            assert tuple(x.index) == defs.VOCALTRACT_PARAMS
        except AttributeError:
            assert len(x) == len(defs.VOCALTRACT_PARAMS)
            series = pd.Series(x, defs.VOCALTRACT_PARAMS)
            self._best_vtp_vparams = series
        else:
            self._best_vtp_vparams = x
        
    def __iter__(self) -> Iterable[Sequence]:
        return self

    def _construct_dataframe(self):
        labels = ["C"] * len(self.consonants) + ["V"]
        mi = pd.MultiIndex.from_tuples(enumerate(labels),
                                       names=Sequence.IDX_NAMES)
        return pd.DataFrame(np.nan,
                            index=mi,
                            columns=defs.TARGETS_TIMECONSTANTS_PARAMS)

    def _constrained_parameter_probability_link(self, df, idx, param):
        """tongue and velum constraints function Constraints1: Tongue
        parameters constraints: whenever the tongue blade parameters
        (TBX/TBY) were adjusted, those of tongue tip and tongue body
        were also modified by 20% with 1% resistance"""
        reference_vtp = (self._best_vtp_vparams
                         if self._best_vtp_vparams is not None
                         else self.bounds.loc["default",
                                              list(defs.VOCALTRACT_PARAMS)])
        if param == "VO":
            linked_param = "TCY"
            neutral_value = reference_vtp[linked_param]
            sampled_value = float(df.loc[idx, linked_param])
            direction = neutral_value - sampled_value
        elif param in ["TCX", "TTX"]:
            linked_param = "TBX"
            neutral_value = reference_vtp[linked_param]
            sampled_value = float(df.loc[idx, linked_param])
            direction = sampled_value - neutral_value
        elif param in ["TCY", "TTY"]:
            linked_param = "TBY"
            neutral_value = reference_vtp[linked_param]
            sampled_value = float(df.loc[idx, linked_param])
            direction = sampled_value - neutral_value
        else:
            raise Exception("Unhandled parameter {}".format(param))
        rval = self.random_state.random_sample()
        if rval < 0.2:
            # 20% chance of moving in the opposite direction
            if direction < 0:
                value = self.random_state.uniform(reference_vtp[param],
                                                  self.bounds[param]["max"])
            else:
                value = self.random_state.uniform(self.bounds[param]["min"],
                                                  reference_vtp[param])
        else:
            if direction >= 0:
                value = self.random_state.uniform(reference_vtp[param],
                                                  self.bounds[param]["max"])
            else:
                value = self.random_state.uniform(self.bounds[param]["min"],
                                                  reference_vtp[param])
        df.loc[idx, param] = value
        return df

    def _derive_tongue_root_y(self, df, idx):
        hyoid_y = float(df.loc[idx, "HY"])
        tongue_body_y = float(df.loc[idx, "TCY"])
        hyoid_tongue_body_centre = (hyoid_y + tongue_body_y) / 2.0
        if (hyoid_tongue_body_centre <= self.bounds["TRY"]["max"]
            and hyoid_tongue_body_centre >= self.bounds["TRY"]["min"]):
            tongue_root_y = hyoid_tongue_body_centre
        elif (abs(hyoid_tongue_body_centre - self.bounds["TRY"]["max"])
              < abs(hyoid_tongue_body_centre - self.bounds["TRY"]["min"])):
            tongue_root_y = self.bounds["TRY"]["max"]
        else:
            tongue_root_y = self.bounds["TRY"]["min"]
        df.loc[idx, "TRY"] = tongue_root_y
        return df

    def _derive_tongue_root_x(self, df, idx):
        hyoid_x = float(df.loc[idx, "HX"])
        tongue_body_x = float(df.loc[idx, "TCX"])
        hyoid_tongue_body_centre = (hyoid_x + tongue_body_x) / 2.0
        tongue_root_x_rightbound = np.min([hyoid_tongue_body_centre,
                                           self.bounds["TRX"]["min"]])
        if tongue_root_x_rightbound > self.bounds["TRX"]["max"]:
            tongue_root_x = self.bounds["TRX"]["max"]
        elif tongue_root_x_rightbound < self.bounds["TRX"]["min"]:
            tongue_root_x = self.bounds["TRX"]["min"]
        else:
            tongue_root_x = self.random_state.uniform(self.bounds["TRX"]["min"],
                                                      tongue_root_x_rightbound)
        df.loc[idx, "TRX"] = tongue_root_x
        return df

    def _vowel_params(self, df):
        ind_params = list(self.INDEPENDENT_PARAMS)
        def_params = list(self.DEFAULT_PARAMS)
        mins = self.bounds[ind_params].loc["min"]
        ranges = self.bounds[ind_params].loc["max"] - mins
        vals = self.random_state.random_sample(len(ind_params))
        vals = (vals * ranges[ind_params]) + mins[ind_params]
        idx = pd.IndexSlice[:, "V"]
        df.loc[idx, ind_params] = vals.to_numpy()
        df.loc[idx, def_params] = (self.bounds[def_params]
                                    .loc["default"]
                                    .to_numpy())
        for param in self.PROBLINK_PARAMS:
            df = self._constrained_parameter_probability_link(df, idx, param)
        df = self._derive_tongue_root_y(df, idx)
        df = self._derive_tongue_root_x(df, idx)
        return df

    def _consonant_params(self, df):
        vidx = pd.IndexSlice[:, "V"]
        cidx = pd.IndexSlice[:, "C"]
        df.loc[cidx, :] = df.loc[vidx, :].to_numpy()
        for row, consonant in zip(df.loc[cidx, :].index, self.consonants):
            ctrl_params = list(consonant_control_params(consonant))
            mins = self.bounds[ctrl_params].loc["min"]
            ranges = self.bounds[ctrl_params].loc["max"] - mins
            vals = self.random_state.random_sample(len(ctrl_params))
            vals = (vals * ranges[ctrl_params]) + mins[ctrl_params]
            df.loc[row, ctrl_params] = vals.to_numpy()
        return df

    def __next__(self) -> Sequence:
        df = self._construct_dataframe()
        df = self._vowel_params(df)
        if self.consonants:
            df = self._consonant_params(df)
        return Sequence(df)

    def sequences(self, num_seqs: int) -> Sequences:
        return Sequences.from_iter(itertools.islice(self, num_seqs),
                                   slurp=True)
