from .models                  import UnumCharFieldModel
from django.forms.models      import ModelForm
from unumcharfield.forms      import UnumCharField
from unumcharfield.unum.units import m

class UnumCharFieldForm(ModelForm):
    formula = UnumCharField(valid_unit=m, max_length=255, min_length=1, max_value=1000*m, min_value=40*m)
    class Meta:
        fields = '__all__'
        model  = UnumCharFieldModel
