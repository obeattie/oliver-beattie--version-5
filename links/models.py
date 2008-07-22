from django.db import models
from django.utils.encoding import force_unicode

from obeattie.generic.tagging.models import Tag as GenericTag, TagManager as GenericTagManager
from obeattie.generic.tagging.fields import TagField
from obeattie.links.managers import LinkManager

class LinkTag(GenericTag):
    """Subclass of Tag (from django_tagging that holds tags specifically for links).
       Being a subclass, the tag is still stored in the global Tag table, as all that is
       stored here is a pointer to the global tag."""
    objects = GenericTagManager()

class Link(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False, db_index=True)
    slug = models.SlugField(blank=False, null=False, unique=True)
    url = models.URLField(max_length=250, blank=False, null=False, verify_exists=True, default='http://', db_index=True)
    description = models.TextField(blank=True, null=True)
    extended_description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=False, auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(blank=True, null=False, auto_now=True, editable=False)
    is_public = models.BooleanField(default=True)
    tags = TagField(blank=True, null=True, model=LinkTag)
    # Custom manager
    objects = LinkManager()
    
    def __unicode__(self):
        return self.title
    
    @property
    def modified(self):
        """Returns a boolean as to whether the link has been modified since it was first
           posted."""
        return self.last_modified != self.created
    
    def _get_full_description(self):
        """Returns the 'full description' for this link. That is, both the description and the
           extended description, if they are present."""
        return u'\n\n'.join([x for x in [self.description, self.extended_description] if x])
    
    def _set_full_description(self, value):
        """Sets the description and extended_description appropriately given a
           'full description'. The first paragraph is assumed to be the description."""
        value = force_unicode(value.split('\n\n'))
        self.description = value[:1]
        self.extended_description = u'\n\n'.join(value[1:])
    full_description = property(_get_full_description, _set_full_description)
