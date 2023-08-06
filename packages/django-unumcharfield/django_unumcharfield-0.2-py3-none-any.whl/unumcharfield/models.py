#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db.models          import CharField, IntegerField, Field
from django.utils.translation  import gettext as _
from unumcharfield             import str2unum
from unumcharfield.validators  import UnumValidator

# Create your models here.
# https://docs.djangoproject.com/en/1.9/howto/custom-model-fields/
class UnumCharField(CharField):
    description = _("Unum Char Field")
    
    def __init__(self, *args, db_collation=None, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.validators.append(UnumValidator())
    
    def from_db_value(self, value, expression, connection, context=None):
        return str2unum(value)
    
    def to_python(self, value):
        return str2unum(super().to_python(value))
    
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return str(value)
    
#     def clean(self, value, model_instance):
#         print('clean')
#         value = self.to_python(value)
#         print('to')
# #         self.validate(str(value), model_instance)
#         self.validate(value, model_instance)
#         print('validate')
#         self.run_validators(value)
#         print('run-valid')
#         return value
#         return CharField.clean(self, value, model_instance)
    
    
#     def db_type(self, connection):
#         return 'varchar(255)'
#     
#     def get_internal_type(self):
#         return 'CharField'
#     
#     def validate(self, value, model_instance):
#         #super(UnumField, self).validate(value, model_instance)
#         return str2unum(value)
#         #return models.CharField.validate(self, value, model_instance)
#     
#     def value_to_string(self, obj):
#         print('value2str')
#         value = self._get_val_from_obj(obj)
#         return self.get_prep_value(value)
