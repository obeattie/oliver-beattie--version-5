from django.db import models

from obeattie.generic.tagging.models import Tag as GenericTag

class BookmarkTag(GenericTag):
    pass

class Bookmark(models.Model):
    """Model for storing links from del.icio.us or another social
       bookmarking service."""
    url = models.URLField(blank=False, null=False, unique=True, db_index=True)
    title = models.CharField(blank=False, null=False, db_index=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=False)
    tags = TagField(BookmarkTag)
    
    class Admin:
        date_hierarchy = 'created'
        list_display = ('url', 'description', 'created', )
        list_filter = ('created', )
        search_fields = ('url', 'description', )
    
    class Meta:
        ordering = ('-created', )
    
    def __unicode__(self):
        return self.title
