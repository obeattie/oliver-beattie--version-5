from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    """A category with which objects can associate themselves."""
    name = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True, null=False)
    description = models.TextField(blank=False, null=False)
    
    class Meta:
        verbose_name_plural = _(u'categories')
    
    def __unicode___(self):
        return self.name

class License(models.Model):
    """A content license."""
    title = models.CharField(max_length=250, blank=False, null=False)
    url = models.URLField(blank=True, null=True, verify_exists=False)
    # Flickr-specific
    flickr_id = models.IntegerField(blank=True, null=True, editable=False)
    
    class Admin:
        pass
    
    def __unicode__(self):
        return self.title
