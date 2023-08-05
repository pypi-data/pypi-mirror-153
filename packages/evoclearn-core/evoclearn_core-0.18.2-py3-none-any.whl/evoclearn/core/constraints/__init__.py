# -*- coding: utf-8 -*-

from functools import partial

from . simple import *


simple_constraints = (tongue_tip_ahead_of_blade,
                      tongue_blade_ahead_of_body,
                      tongue_blade_above_body)

all_constraints = simple_constraints + (vowel_voiced,)
