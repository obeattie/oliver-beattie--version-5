"""Django-admin-related stuff for the metadata application."""
from django.contrib import admin

from obeattie.metadata import models as metadata_models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', )
    prepopulated_fields = { 'slug': ('name', ) }
    search_fields = ('name', 'slug', 'description', )
admin.site.register(metadata_models.Category, CategoryAdmin)

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'flickr_id', )
    search_fields = ('title', 'url', 'flickr_id', )
admin.site.register(metadata_models.License, LicenseAdmin)
