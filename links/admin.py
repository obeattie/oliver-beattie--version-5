"""Django-admin-related stuff for the links application."""
from django.contrib import admin

from obeattie.links import models as links_models

class LinkAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('title', 'url', 'description', 'created', 'last_modified', )
    list_filter = ('created', 'last_modified', 'is_public', )
    search_fields = ('title', 'url', 'description', )
admin.site.register(links_models.Link, LinkAdmin)
