"""Blog-related model managers."""
import datetime

from django.db import models

class PostManager(models.Manager):
    """Manager for posts."""
    
    def get_public(self):
        """The public Post objects."""
        return self.model.objects.filter(is_public=True)
    public = property(get_public)
    
    def get_published(self):
        """The Post objects which have been publically published."""
        return self.model.objects.public.filter(published__lte=datetime.datetime.now())
    