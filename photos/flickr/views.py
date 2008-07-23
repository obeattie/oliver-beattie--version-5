"""Miscellaneous Flickr views."""
from django.http import HttpResponseRedirect

from obeattie.miscellaneous.utils.requests import check_key
from obeattie.photos.flickr.requests import authentication

def begin_authorization(request, permissions='delete'):
    """Redirects to the Flickr authorization page."""
    return HttpResponseRedirect(authentication.build_authentication_url(permissions=permissions))

def complete_authorization(request):
    """Completes the authorization with Flickr, and displays the resulting
       data."""
    check_key(request.GET, 'frob')
