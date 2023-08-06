from django import forms
from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin
from djangoldp.models import Model
from djangoldp_hiphopcommunity.models import Project

class ProjectAdmin(DjangoLDPAdmin):
    list_display= ('name', 'visible')

admin.site.register(Project, ProjectAdmin)