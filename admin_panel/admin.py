from django.contrib.admin import ModelAdmin
from django.contrib import admin

from admin_panel.models import *


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    ...


@admin.register(Events)
class EventsAdmin(ModelAdmin):
    ...


@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    ...
