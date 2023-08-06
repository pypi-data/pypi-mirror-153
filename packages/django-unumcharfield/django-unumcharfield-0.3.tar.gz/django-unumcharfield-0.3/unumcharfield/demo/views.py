from .                         import models, forms
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

# Create your views here.
class UnumCharFieldForm(UpdateView):
    model = models.UnumCharFieldModel
    form_class = forms.UnumCharFieldForm
    success_url = '.'

class UnumCharFieldTestList(ListView):
    model = models.UnumCharFieldModel
