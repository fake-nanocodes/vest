from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass

