"""Miscellaneous Flickr views."""
from django.http import HttpResponseRedirect

BASE_AUTH_URL = u'http://flickr.com/services/auth/'

def begin_authorization(request, permissions='delete'):
    """Redirects to the Flickr authorization page."""
    url = BASE_AUTH_URL
    
    return HttpResponseRedirect()
