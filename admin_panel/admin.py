from django.contrib.admin import ModelAdmin
from django.contrib import admin

from admin_panel.sqlalchemy_models import *
from admin_panel.models import *


@admin.register(Company)
class CompanyAdmin(ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(CompanyAdmin, self).get_queryset(request)
        qs = super(CompanyAdmin, self).get_queryset(request)
        return qs.filter(users=request.user)


@admin.register(Events)
class EventsAdmin(ModelAdmin):
    ...


@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    ...


@admin.register(CompanyUser)
class CompanyUserAdminAdmin(ModelAdmin):
    ...
