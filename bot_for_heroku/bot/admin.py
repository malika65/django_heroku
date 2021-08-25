from django.contrib import admin

from .models import People
from import_export.admin import ExportActionMixin

@admin.register(People)
class NewsAdmin(ExportActionMixin, admin.ModelAdmin):

    list_display = ("name", "telephone","oblast","raion","doljnost","sale")
    list_display_links = ("name",)