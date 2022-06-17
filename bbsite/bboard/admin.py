from django.contrib import admin

from .models import Bb, Rubric

class BbAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'rubric']
    list_display_links = ['title', 'price']
    search_fields = ['title', 'content']

admin.site.register(Bb, BbAdmin)

admin.site.register(Rubric)
