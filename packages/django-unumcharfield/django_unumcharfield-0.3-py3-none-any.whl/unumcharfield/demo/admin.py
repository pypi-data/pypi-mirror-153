from .forms         import UnumCharFieldForm
from .models        import UnumCharFieldModel
from django.contrib import admin

# Register your models here.
class UnumCharFieldAdmin(admin.ModelAdmin):
    form = UnumCharFieldForm

admin.site.register(UnumCharFieldModel, UnumCharFieldAdmin)