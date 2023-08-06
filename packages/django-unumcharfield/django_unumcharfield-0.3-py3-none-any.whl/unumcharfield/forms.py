#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.forms             import TextInput, CharField, IntegerField
from django.utils.translation import gettext as _
from unumcharfield            import str2unum
from unumcharfield.validators import UnumValidator, UnumCompatibilityValidator

class UnumCharField(CharField, IntegerField):
    description = _("Unum Char Field")
    widget      = TextInput
    
    def __init__(self, valid_unit=None, **kwargs):
        if 'max_value' in kwargs:
            kwargs['max_value'] = str2unum(kwargs['max_value'])
        if 'min_value' in kwargs:
            kwargs['min_value'] = str2unum(kwargs['min_value'])
        super().__init__(**kwargs)
        
        self.validators.append(UnumValidator())
        
        self.valid_unit = str2unum(valid_unit)
        if valid_unit:
            self.validators.append(UnumCompatibilityValidator(self.valid_unit))
    
    def to_python(self, value):
        """Return a Unum object."""
        return str2unum(super().to_python(value))
