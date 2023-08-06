from django.db            import models
from unumcharfield.models import UnumCharField

class UnumCharFieldTest(models.Model):
    formula = UnumCharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return str(self.formula)
