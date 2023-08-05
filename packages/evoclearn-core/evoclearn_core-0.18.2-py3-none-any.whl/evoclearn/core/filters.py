# -*- coding: utf-8 -*-
""" Functions that map Sequences to Sequences (not necessarily of the same
length) """

from typing import Iterable, Callable

from . import Sequence

from .mappings import satisfies_constraints
from .constraints import simple_constraints


def discard_by_constraints(
    seqs: Iterable[Sequence],
    constraints: Iterable[Callable[[Sequence], bool]]=simple_constraints
    ) -> Iterable[Sequence]:
    filt = (seq for seq in seqs
            if satisfies_constraints(seq, constraints))
    return filt
