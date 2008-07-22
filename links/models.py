from django.db import models
from django.utils.encoding import force_unicode

class Link(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False, db_index=True)
    description = models.TextField(blank=True, null=True)
    extended_description = models.TextField(blank=True, null=True)
    
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
