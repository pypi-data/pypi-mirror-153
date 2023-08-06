#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unum                     import Unum, units
from unumcharfield.validators import UnumValidationError

# These settings make possible the conversion of strings in Unum objects.
# It was necessary modify Unum code to make the conversion possible.
# It is not recomended edit these settings.
# 
Unum.UNIT_SEP     = "*"
Unum.UNIT_FORMAT  = "%s"
Unum.UNIT_INDENT  = "*"
Unum.AUTO_NORM    = True
Unum.UNIT_POW_SEP = "**"
# Unum.UNIT_DIV_SEP = None
# Unum.UNIT_HIDE_EMPTY = True
# Unum.VALUE_FORMAT = "%15.7f"
# Unum.UNIT_SORTING = True

def str2unum(unum_str):
    """Convert string to Unum object."""
    # http://stackoverflow.com/questions/13611851/casting-string-to-unit-object-in-python
    # http://lybniz2.sourceforge.net/safeeval.html
    # http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
    
    if isinstance(unum_str, Unum) or unum_str is None:
        return unum_str
    if isinstance(unum_str, str):
        if '__' in unum_str:
            raise ValueError("Won't do this with underscores...it's unsafe!")
    else:
        raise ValueError("It is not a string or Unum instance!")
    safe_dict = dict((x,y) for x,y in units.__dict__.items() if '__' not in x)
    try:
        obj = eval(unum_str, {'__builtins__':{}}, safe_dict)
    except:
        obj = Unum()
    return obj
