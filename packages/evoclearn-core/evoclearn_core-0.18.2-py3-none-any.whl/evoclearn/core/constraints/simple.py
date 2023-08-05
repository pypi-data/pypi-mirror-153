# -*- coding: utf-8 -*-

from inspect import getmembers, isfunction
from functools import partial

from . import generic


for funcname, func in [(name, obj)
                       for name, obj
                       in getmembers(generic)
                       if isfunction(obj) and not name.startswith("_")]:
    globals()[funcname] = partial(lambda *args, f, **kwargs: f(*args, **kwargs) <= 0.0, f=func)
