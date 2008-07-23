"""Model managers for the links application."""
from django.db import models
from django.db.models.query import QuerySet

class LinkQuerySet(QuerySet):
    """Custom QuerySet that implements some custom shit for links."""
    def get_public(self):
        """Returns a filtered LinkQuerySet that only contains the public
           links."""
        return self._filter_or_exclude(False, is_public=True)

class LinkManager(models.Manager):
    def get_query_set(self):
        return LinkQuerySet(self.model)
    
    def get_public(self):
        return self.get_query_set().get_public()
