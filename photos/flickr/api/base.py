"""Flickr request classes. Provides a base for all of the request methods."""
import hashlib

from django.conf import settings
from django.utils.datastructures import SortedDict
from django.utils.http import urlencode

class FlickrParameters(SortedDict):
    """A SortedDict subclass which helps in generating
       the parameters to pass in a Flickr request."""
    def __init__(self, data={}, *args, **kwargs):
        data.update({ 'api_key': settings.FLICKR_API_KEY })
        return super(FlickrParameters, self).__init__(data, *args, **kwargs)
    
    def sorted_items(self):
        """Sorts self.items() in ascending order and then returns the result."""
        def item_compare(x, y):
            if x[0] > y[0]:
                return 1
            elif x[0] == y[0]:
                return 0
            else:
                return -1
        
        return sorted(self.items(), item_compare)
    
    def hashed(self):
        return hashlib.md5(u'%(secret)s%(params)s' % {
            'secret': settings.FLICKR_API_SECRET,
            'params': ''.join([u'%s%s' % (i[0], i[1]) for i in self.sorted_items()]),
        }).hexdigest()
    
    def urlencode(self):
        """Returns the urlencoded result of the parameters, ready to append in a query
           string or similar."""
        parameters = SortedDict()
        for param in self.sorted_items():
            parameters[param[0]] = param[1]
        parameters['api_sig'] = self.hashed()
        return urlencode(parameters)

class FlickrRequest(object):
    """An abstract base class which encapsulates a request to be made to the Flickr API."""
    method = None
    
    def __init__(self, params, *args, **kwargs):
        # Enforce the abstract baseyness :)
        assert not isinstance(self, FlickrRequest)
        # If params is not yet FlickrParameters, make them so
        if not isinstance(params, FlickrParameters):
            params = FlickrParameters(params)
        # ...now store the params
        self.params = params
        return super(FlickrRequest, self).__init__(*args, **kwargs)
