"""Describe project admin."""
from django.contrib import admin

from bboard.models import Bb, Rubric


class BbAdmin(admin.ModelAdmin):
    """Describe form by admin setting."""

    list_display = ['title', 'price', 'rubric']
    list_display_links = ['title', 'price']
    search_fields = ['title', 'content']

admin.site.register(Bb, BbAdmin)

admin.site.register(Rubric)
