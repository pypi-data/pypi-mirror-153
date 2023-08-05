# -*- coding: utf-8 -*-

from typing import Iterable, Optional
import itertools
from collections import defaultdict
import json

import pandas as pd
import numpy as np

from .. import Sequence, Sequences, TARGETS_TIMECONSTANTS_PARAMS
from .. utils import standard_param_order


def paramkeysvals_by_label(params: dict):
    """`params` is a dict with label-param keys"""
    params_labs = set([k.split("-")[0] for k in params])
    pkeys_by_lab = {}
    pvals_by_lab = {}
    for lab in params_labs:
        d = {k.split("-")[1]: v
             for k, v in params.items()
             if k.split("-")[0] == lab}
        assert len(d) == len(set(d).intersection(TARGETS_TIMECONSTANTS_PARAMS))
        keys = list(d)
        vals = [d[k] for k in keys]
        pkeys_by_lab[lab] = keys
        pvals_by_lab[lab] = vals
    return pkeys_by_lab, pvals_by_lab


def reorder_labels_for_construction(labels, copy):
    """Currently can only specify a single copy source and we need to
    sample/process the source label first
    """
    if copy is None:
        copy_src = None
    elif type(copy) is str:
        copy_src = copy
    elif type(copy) is list or type(copy) is dict:
        raise NotImplementedError
        _labs = set(k.split("-")[0] for k in copy)
        assert len(_labs) == 1
        copy_src = _labs.pop()
    else:
        raise Exception("Invalid `copy` input...")
    if copy_src is not None:
        assert copy_src in labels
        labels.insert(0, labels.pop(labels.index(copy_src)))
    return labels


def sort_uniq_paramkeys(paramkeys: list, lab_order="CV"):
    lab_order = list(lab_order) if lab_order is not None else []
    paramkeys = list(set(paramkeys))
    d = defaultdict(list)
    for lab, param in (pkey.split("-") for pkey in paramkeys):
        d[lab].append(param)
    d = dict(d)
    for lab in d:
        d[lab] = standard_param_order(d[lab])
    sorted_paramkeys = []
    for lab in lab_order:
        if lab in d:
            for param in d.pop(lab):
                sorted_paramkeys.append(f"{lab}-{param}")
    for lab in sorted(d):
        for param in d[lab]:
            sorted_paramkeys.append(f"{lab}-{param}")
    return sorted_paramkeys
            

def sequence_to_params(seq: Sequence,
                       paramkeys: Optional[list]=None) -> dict:
    """Convert a sequence into a simple flat dictionary mapping
    "lab-param" to values. If paramkeys are given then only these
    values will be returned.
    """
    params = {}
    if paramkeys is not None:
        for pkey in paramkeys:
            lab, param = pkey.split("-")
            idx = pd.IndexSlice[:, lab]
            params[pkey] = float(seq.loc[idx, param])
    else:
        for lab in seq.index.get_level_values("lab"):
            idx = pd.IndexSlice[:, lab]
            for param in seq.columns:
                params[f"{lab}-{param}"] = float(seq.loc[idx, param])
    return params


def sequence_to_paramvalues(seq: Sequence, paramkeys: list) -> list:
    """Return a list of param values corresponding to the paramkeys"""
    params = sequence_to_params(seq, paramkeys)
    return [params[k] for k in paramkeys]


def params_to_sequence(params: dict,
                       baseseq: Optional[Sequence]=None,
                       copy=None,
                       label_construction_order=None) -> Sequence:
    # Validate params and split by label and keys/vals:
    pkeys_by_lab, pvals_by_lab = paramkeysvals_by_label(params)
    if baseseq is None:
        if copy is not None or label_construction_order is not None:
            raise ValueError("`copy` and `label_construction_order` not"
                             " expected without `baseseq`...")
        # Construct minimal sequence (this is useful to apply mappings
        # that operate on Sequence, e.g. normalisation functions)
        labels = list(pkeys_by_lab)
        params = set(itertools.chain(*pkeys_by_lab.values()))
        seq = Sequence.from_spec(params, labels)
        for lab in pkeys_by_lab:
            idx = pd.IndexSlice[:, lab]
            seq.loc[idx, pkeys_by_lab[lab]] = pvals_by_lab[lab]
    else:
        seq = baseseq.copy()
        seq_labels = list(seq.index.get_level_values("lab"))
        if label_construction_order is None:
            label_construction_order = reorder_labels_for_construction(seq_labels, copy)
        else:
            assert set(seq_labels) == set(label_construction_order)
        for i, lab in enumerate(label_construction_order):
            idx = pd.IndexSlice[:, lab]
            # Copy from source label first:
            if i > 0 and copy is not None:
                srcidx = pd.IndexSlice[:, copy]
                seq.loc[idx, :] = seq.loc[srcidx, :].to_numpy()
            if lab in pkeys_by_lab:
                seq.loc[idx, pkeys_by_lab[lab]] = pvals_by_lab[lab]
    return seq


def construction_spec_to_json(cspec: dict) -> str:
    required = {"baseseq", "copy"}
    d = {k: cspec[k] for k in required}
    if "label_construction_order" in cspec:
        d["label_construction_order"] = cspec["label_construction_order"]
    d["baseseq"] = d["baseseq"].to_json()
    return json.dumps(d)


def construction_spec_from_json(s: str) -> dict:
    d = json.loads(s)
    d["baseseq"] = Sequence.from_json(d["baseseq"])
    return d


class TiedTargets(object):
    """This creates Sequences that have a full set of parameters by
       combining a base Sequence with a subset of free
       parameters. Free parameters are specified by dictionary of
       bounds and keys are "label-param"

       `copy` should do the following:
            - If a SEGMENT is given, copy all params from that segment
              to all other segments before replacing with
              free/sampled
            - If a LIST OF PARAMKEYS are given, copy only those to all
              other segments before replacing (may only source from 1
              segment)
            - If a DICT OF PARAMKEYS are given, copy from source to
              targets before replacing (may only source from 1 segment)

    """
    def __init__(self,
                 free_param_bounds: dict,
                 baseseq: Sequence,
                 copy=None,
                 seed: int=None):
        baseseq_labels = self._validate_baseseq_get_labels(baseseq)
        self.baseseq = baseseq.copy()
        self._bounds = self._validate_bounds_get_by_label(free_param_bounds,
                                                          baseseq_labels)
        self.free_param_bounds = free_param_bounds
        baseseq_labels = reorder_labels_for_construction(baseseq_labels, copy)
        self.label_construction_order = tuple(baseseq_labels)
        self.copy = copy
        self.seed = seed
        self.random_state = np.random.RandomState(self.seed)

    def __iter__(self) -> Iterable[Sequence]:
        return self

    def __next__(self) -> Sequence:
        sampled_params = {}
        for lab in self.baseseq.index.get_level_values("lab"):
            bounds = self._bounds.get(lab)
            if bounds is not None:
                sampled_values = self.random_state.random_sample(len(bounds.columns))
                ranges = bounds.loc["max"] - bounds.loc["min"]
                sampled_values = sampled_values * ranges + bounds.loc["min"]
                for param, val in sampled_values.to_dict().items():
                    sampled_params[f"{lab}-{param}"] = val
        return params_to_sequence(sampled_params,
                                  self.baseseq,
                                  self.copy,
                                  self.label_construction_order)
    
    def sequences(self, num_seqs: int) -> Sequences:
        return Sequences.from_iter(itertools.islice(self, num_seqs),
                                   slurp=True)

    def to_json(self):
        return json.dumps({"baseseq": self.baseseq.to_json(),
                           "free_param_bounds": self.free_param_bounds,
                           "label_construction_order": self.label_construction_order,
                           "copy": self.copy,
                           "seed": self.seed})

    @classmethod
    def from_json(cls, s):
        constr_args = json.loads(s)
        constr_args["baseseq"] = Sequence.from_json(constr_args["baseseq"])
        constr_args.pop("label_construction_order")
        return cls(**constr_args)
    
    @staticmethod
    def _validate_baseseq_get_labels(seq):
        """Check that all parameters exist and segment labels not in conflict
        with local naming conventions
        """
        assert list(seq.columns) == list(TARGETS_TIMECONSTANTS_PARAMS)
        labels = list(seq.index.get_level_values("lab"))
        assert len(set(labels)) == len(labels)
        assert not any(["-" in lab for lab in labels])
        return labels

    @staticmethod
    def _validate_bounds_get_by_label(param_bounds, baseseq_labels):
        """Split by segment label, validate parameters and store ranges as dataframes"""
        bounds_by_label = {}
        labs = set([k.split("-")[0] for k in param_bounds])
        for lab in labs:
            d = {k.split("-")[1]: v
                 for k, v in param_bounds.items()
                 if k.split("-")[0] == lab}
            assert len(d) == len(set(d).intersection(TARGETS_TIMECONSTANTS_PARAMS))
            bounds_by_label[lab] = pd.DataFrame(d,
                                                index=["min", "max"],
                                                columns=standard_param_order(d))
        assert set(bounds_by_label).issubset(baseseq_labels)
        return bounds_by_label
