from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    pass