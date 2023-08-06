#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.exceptions   import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from unumcharfield.unum       import Unum, units

class UnumValidationError(ValidationError):
    """
    Unum Validation Error.
    """
    message = _('Enter a Unum Object.')
    
    def __init__(self, message=message, code=None, params=None):
        super().__init__(message, code, params)

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
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__))

@deconstructible
class UnumDimensionValidator(UnumValidator):
    """
    Validate if the input has the same Unum dimension, otherwise raise UnumValidationError.
    """
    messages = {
        'invalid': _('Enter a Unum Object.'),
        'dimension': _(
            'Ensure dimension is equal than %(dim).',
            'Ensure dimension is equal than %(dim).',
            'dim'
        ),
    }
     
    def __init__(self, dimension=None, **kwargs):
        self.dimension = dimension
        super().__init__(**kwargs)
     
    def __call__(self, value):
        super().__call__(value)
        if dimsys_SI.equivalent_dims(self.dimension, value):
            raise ValidationError(
                self.messages['dimension'],
                code='dimension',
                params={'dim': (self.dimension)},
            )
 
    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.dimension == other.dimension
        )

