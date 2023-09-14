from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    pass
    # def get_readonly_fields(self, request, obj=None):
    #     # Get all field names from the model
    #     all_fields = [field.name for field in obj.__class__._meta.fields]
    #     return all_fields

