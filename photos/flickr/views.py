"""Miscellaneous Flickr views."""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from obeattie.miscellaneous.utils.requests import check_key
from obeattie.photos.flickr.api import authentication, FlickrJSONRequest

@login_required
def begin_authorization(request, permissions='delete'):
    """Redirects to the Flickr authorization page."""
    return HttpResponseRedirect(authentication.build_authentication_url(permissions=permissions))

@login_required
def complete_authorization(request):
    """Completes the authorization with Flickr, and displays the resulting
       data."""
    check_key(request.GET, 'frob')
    request = authentication.getToken({
        'frob': request.GET['frob'],
    })
    return HttpResponse(unicode(request.send().decoded))
