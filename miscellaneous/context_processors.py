"""Miscellaneous context processors."""
from django.contrib.sites.models import Site

def site(request):
    """Adds a site variable to the template context which is the active
       Site object."""
    return { 'site': Site.objects.get_current() }
