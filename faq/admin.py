from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass

