"""Authentication calls for the Flickr API."""
from obeattie.photos.flickr.api import base

def build_authentication_url(permissions='delete'):
    """Returns a URL where a user can be redirected to for authenticating the site
       to use their account details."""
    # Make sure the permissions requested are legal
    assert permissions in ('read', 'write', 'delete', )
    return u'http://www.flickr.com/services/auth/?%s' % base.FlickrParameters({ 'perms': permissions }).urlencode()

class GetToken(base.FlickrJSONRequest):
    method = 'flickr.auth.getToken'
    required_params = ['frob', ]
