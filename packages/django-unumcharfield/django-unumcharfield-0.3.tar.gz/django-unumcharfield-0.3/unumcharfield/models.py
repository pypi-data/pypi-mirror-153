#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db.models         import CharField
from django.utils.translation import gettext as _
from unumcharfield            import str2unum
from unumcharfield.validators import UnumValidator, UnumCompatibilityValidator

# Create your models here.
# https://docs.djangoproject.com/en/1.9/howto/custom-model-fields/
class UnumCharField(CharField):
    description = _("Unum Char Field")
    
    def __init__(self, valid_unit=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(UnumValidator())
        if valid_unit:
            self.validators.append(UnumCompatibilityValidator(valid_unit))
    
    def from_db_value(self, value, expression, connection, context=None):
        return str2unum(value)
    
    def to_python(self, value):
        return str2unum(super().to_python(value))
    
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return str(value)
