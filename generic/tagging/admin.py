from django.contrib import admin
from obeattie.generic.tagging.models import Tag, TaggedItem

admin.site.register(TaggedItem)
admin.site.register(Tag)
