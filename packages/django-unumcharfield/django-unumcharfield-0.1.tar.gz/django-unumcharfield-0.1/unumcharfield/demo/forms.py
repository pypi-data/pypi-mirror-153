from .                   import models
from django.forms.models import ModelForm

class UnumCharFieldTest(ModelForm):
    class Meta:
        model = models.UnumCharFieldTest
        fields = ['formula',]
