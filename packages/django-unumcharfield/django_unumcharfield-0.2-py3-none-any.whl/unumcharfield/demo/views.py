from .                         import models, forms
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

# Create your views here.
class UnumCharFieldTest(UpdateView):
    model = models.UnumCharFieldTest
    form_class = forms.UnumCharFieldTest
    success_url = '.'

class UnumCharFieldTestList(ListView):
    model = models.UnumCharFieldTest
