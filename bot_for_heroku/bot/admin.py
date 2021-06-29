from django.contrib import admin

from .models import People


@admin.register(People)
class NewsAdmin(admin.ModelAdmin):

    list_display = ("name", "telephone","oblast","raion","doljnost","sale")
    list_display_links = ("name",)