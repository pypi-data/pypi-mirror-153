from django.db.models     import Model
from unumcharfield.models import UnumCharField

class UnumCharFieldModel(Model):
    formula = UnumCharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return str(self.formula)
