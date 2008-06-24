import datetime

from django.db import models

from obeattie.generic.tagging.fields import TagField
from obeattie.generic.tagging.models import Tag as GenericTag, TagManager as GenericTagManager

class BookmarkTag(GenericTag):
    objects = GenericTagManager()

class Bookmark(models.Model):
    """Model for storing links from del.icio.us or another social
       bookmarking service."""
    url = models.URLField(blank=False, null=False, unique=True, db_index=True)
    title = models.CharField(blank=False, null=False, max_length=250, db_index=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=False)
    tags = TagField(BookmarkTag)
    
    def save(self, *args, **kwargs):
        # Set self.created if it isn't already
        self.created = self.created or datetime.datetime.now()
        return super(Bookmark, self).save(*args, **kwargs)
    
    class Admin:
        date_hierarchy = 'created'
        list_display = ('url', 'description', 'created', )
        list_filter = ('created', )
        search_fields = ('url', 'description', )
    
    class Meta:
        ordering = ('-created', )
    
    def __unicode__(self):
        return self.title
