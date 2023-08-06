#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.validators           import MaxValueValidator, MinValueValidator
from django.forms                     import TextInput, CharField, Field
from django.utils.translation         import gettext as _
from unumcharfield                    import str2unum
from unumcharfield.validators         import UnumValidator

class UnumCharField(CharField):
    description = _("Unum Char Field")
    widget      = TextInput
    
    def __init__(self, *, max_value=None, min_value=None, max_length=None,
                 min_length=None, strip=True, empty_value=0, **kwargs):
        self.max_length  = max_length
        self.min_length  = min_length
        self.strip       = strip
        self.empty_value = empty_value
        Field.__init__(self, **kwargs)
        
        self.validators.append(UnumValidator())
        if min_value is not None:
            self.validators.append(MinValueValidator(str2unum(min_value)))
        if max_value is not None:
            self.validators.append(MaxValueValidator(str2unum(max_value)))
    
    def to_python(self, value):
        """Return a Unum object."""
        return str2unum(super().to_python(value))

from django.forms.fields              import IntegerField
from unumcharfield.validators         import UnumDimensionValidator
 
class UnumDimensionCharField(CharField, IntegerField):
    description = "Unum Char Field with dimensional verification"
     
    def __init__(self, *, dimension=None, **kwargs):
        if kwargs.get('min_value'):
            kwargs['min_value'] = str2unum(kwargs.get('min_value'))
        if kwargs.get('max_value'):
            kwargs['max_value'] = str2unum(kwargs.get('max_value'))
        super().__init__(**kwargs)
         
        self.validators.append(UnumValidator())
         
        self.dimension = dimension
        if self.dimension:
            self.validators.append(UnumDimensionValidator(dimension))
     
    def to_python(self, value):
        """Return a Unum object."""
         
        if value in self.empty_values:
            return None
        value = str(value)
        if self.strip:
            value = value.strip()
        if self.localize:
            value = formats.sanitize_separators(value)
        try:
            value = str2unum(value)
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value
     
    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, TextInput):
            if self.min_value is not None:
                attrs['min'] = self.min_value
            if self.max_value is not None:
                attrs['max'] = self.max_value
        return attrs
    def clean(self, value):
        return Field.clean(self, value)
    def validate(self, value):
        super().validate(value)
