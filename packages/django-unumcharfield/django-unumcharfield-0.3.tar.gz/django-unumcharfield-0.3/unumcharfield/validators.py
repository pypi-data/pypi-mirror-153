#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.exceptions   import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from unumcharfield.unum       import Unum

messages = {
            'invalid'     : _('Enter an Unum Object.'),
            'incompatible': _('%(other_unit)s is not compatible with %(valid_unit)s.'),
            }

class UnumValidationError(ValidationError):
    """
    Unum Validation Error.
    """
    
    def __init__(self, message='invalid', params=None):
        super().__init__(message=messages[message], code=message, params=params)

@deconstructible
class UnumValidator:
    """
    Validate if the input is an instance of Unum, otherwise raise UnumValidationError.
    """
    
    def __init__(self):
        pass
    
    def __call__(self, value):
        if not isinstance(value, Unum):
            raise UnumValidationError()
        return value
    
    def __eq__(self, other):
        return isinstance(other, self.__class__)

@deconstructible
class UnumCompatibilityValidator(UnumValidator):
    """
    Validate if the input has the same Unum unit type (length, mass, etc),
    otherwise raise UnumValidationError.
    """
    
    def __init__(self, valid_unit=None, **kwargs):
        self.valid_unit = super().__call__(valid_unit)
        super().__init__(**kwargs)
    
    def __call__(self, value):
        super().__call__(value)
        if not self.valid_unit.compatible(value):
            raise UnumValidationError('incompatible',
                                      params={'valid_unit': self.valid_unit, 'other_unit': value})
        return value
    
    def __eq__(self, other):
        return self.valid_unit == other.valid_unit
