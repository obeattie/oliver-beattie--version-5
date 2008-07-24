"""Flickr request classes. Provides a base for all of the request methods."""
import hashlib, syslog, traceback, urllib

from django.conf import settings
from django.utils.datastructures import SortedDict
from django.utils.http import urlencode
from django.utils import simplejson

from obeattie.photos.flickr.api import pagination

FLICKR_API_ENDPOINT = u'http://api.flickr.com/services/rest/'

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

#          _______   ________   ______   _______    ______   __    __   ______   ________ 
#        /       \ /        | /      \ /       \  /      \ /  \  /  | /      \ /        | 
#        $$$$$$$  |$$$$$$$$/ /$$$$$$  |$$$$$$$  |/$$$$$$  |$$  \ $$ |/$$$$$$  |$$$$$$$$/  
#        $$ |__$$ |$$ |__    $$ \__$$/ $$ |__$$ |$$ |  $$ |$$$  \$$ |$$ \__$$/ $$ |__     
#        $$    $$< $$    |   $$      \ $$    $$/ $$ |  $$ |$$$$  $$ |$$      \ $$    |    
#        $$$$$$$  |$$$$$/     $$$$$$  |$$$$$$$/  $$ |  $$ |$$ $$ $$ | $$$$$$  |$$$$$/     
#        $$ |  $$ |$$ |_____ /  \__$$ |$$ |      $$ \__$$ |$$ |$$$$ |/  \__$$ |$$ |_____  
#        $$ |  $$ |$$       |$$    $$/ $$ |      $$    $$/ $$ | $$$ |$$    $$/ $$       | 
#        $$/   $$/ $$$$$$$$/  $$$$$$/  $$/        $$$$$$/  $$/   $$/  $$$$$$/  $$$$$$$$/  
#

class FlickrResponse(object):
    """Another sorta-abstracty base class which encapsulates a response from
       the Flickr API."""
    def __init__(self, request, response, *args, **kwargs):
        # Abstractyness, baby!
        assert not self.__class__ is FlickrResponse
        # Request must be an instance of FlickrRequest, and response
        # must be a file-like object.
        assert isinstance(request, FlickrRequest)
        self.request = request
        self.raw_response = response.read()
        return super(FlickrResponse, self).__init__(*args, **kwargs)
    
    def decode(self):
        raise NotImplementedError

class FlickrJSONResponse(FlickrResponse):
    def clean_response(self, input):
        """Removes those disgusting _content attributes from the decoded
           JSON from Flickr. I don't get why the fuck they were necessary in
           the first place... Recursive function."""
        if isinstance(input, dict):
            if len(input.items()) and '_content' in input:
                return input['_content']
            else:
                for item in input.items():
                    input[item[0]] = self.clean_response(item[1])
        elif isinstance(input, (list, tuple)):
            index = 0
            for item in input:
                input[index] = self.clean_response(item)
                index += 1
        return input
    
    @property
    def decoded(self):
        """Return the decoded JSON."""
        if not hasattr(self, '_decoded'):
            self._decoded = self.clean_response(simplejson.loads(self.raw_response))
        return self._decoded

#         _______   ________   ______   __    __  ________   ______   ________ 
#        /       \ /        | /      \ /  |  /  |/        | /      \ /        |
#        $$$$$$$  |$$$$$$$$/ /$$$$$$  |$$ |  $$ |$$$$$$$$/ /$$$$$$  |$$$$$$$$/ 
#        $$ |__$$ |$$ |__    $$ |  $$ |$$ |  $$ |$$ |__    $$ \__$$/    $$ |   
#        $$    $$< $$    |   $$ |  $$ |$$ |  $$ |$$    |   $$      \    $$ |   
#        $$$$$$$  |$$$$$/    $$ |_ $$ |$$ |  $$ |$$$$$/     $$$$$$  |   $$ |   
#        $$ |  $$ |$$ |_____ $$ / \$$ |$$ \__$$ |$$ |_____ /  \__$$ |   $$ |   
#        $$ |  $$ |$$       |$$ $$ $$< $$    $$/ $$       |$$    $$/    $$ |   
#        $$/   $$/ $$$$$$$$/  $$$$$$  | $$$$$$/  $$$$$$$$/  $$$$$$/     $$/    
#                                 $$$/

class FlickrRequest(object):
    """An abstract base (sorta) class which encapsulates a request to be made to
       the Flickr API."""
    method = None
    response_handler = None
    default_params = { 'api_key': settings.FLICKR_API_KEY, 'auth_token': settings.FLICKR_API_TOKEN }
    forced_params = {}
    required_params = ['method', ]
    excluded_params = set() # Keys are unique
    optional_params = []
    pagination_params = {} # Should have the keys 'page_key' and 'paginate_by_key', and optionally 'max_per_page'
    
    def __init__(self, params, excluded_params=[], *args, **kwargs):
        # Enforce the abstract baseyness :)
        assert not self.__class__ is FlickrRequest
        # If params is not yet FlickrParameters, make them so
        if not isinstance(params, FlickrParameters):
            params = FlickrParameters(params)
        # Check all of the params are valid for this call
        valids = self.get_valid_params()
        for key in params.keys():
            assert key in valids
        del valids # No longer needed
        # Now populate any default arguments
        for item in self.default_params.items():
            params.setdefault(item[0], item[1])
        # ...and any forced arguments
        params.update(self.forced_params)
        params.update({ 'method': self.method or params['method'] })
        # Check for the presence of required params
        for key in self.get_required_params():
            assert key in params
        # Finally remove any explicitly excluded params, these are removed at
        # the request of the user in spite of what the class definition says.
        self.excluded_params.update(excluded_params)
        for key in self.excluded_params:
            params.pop(key, None)
        # All good! Now store the params
        self.params = params
        return super(FlickrRequest, self).__init__(*args, **kwargs)
    
    def get_valid_params(self):
        params = set()
        params.update(self.required_params)
        params.update(self.optional_params)
        params.update(self.forced_params.keys())
        params.update(self.default_params.keys())
        params.update([i for i in [self.pagination_params.get('page_key', None), self.pagination_params.get('paginate_by_key', None)] if i])
        return params
    
    def get_required_params(self):
        params = set()
        params.update(self.required_params)
        try:
            params.update(super(FlickrRequest, self).get_required_params())
        except AttributeError:
            pass
        return params
    
    def build_url(self):
        """Returns the URL for making the request."""
        return u'%s?%s' % (FLICKR_API_ENDPOINT, self.params.urlencode())
    
    def send(self):
        """Sends the request and returns the proper (instantiated) response
           handler."""
        try:
            self._response = self.response_handler(request=self, response=urllib.urlopen(self.build_url()))
        except Exception, e:
            # Syslog any errors here
            syslog.syslog(syslog.LOG_ERR, traceback.format_exc())
            # And re-raise
            raise e
        return self._response
    
    def get_paginator(self):
        retrurn pagination.FlickrAPIPaginator(request=self)
    
    @property
    def response(self):
        """Returns the instantiated response handler for this request. If the request has
           already been sent, then the cached result from the previous request will be used."""
        if hasattr(self, '_response'):
            return self._response
        else:
            return self.send()

class FlickrJSONRequest(FlickrRequest):
    """Subclass of FlickrRequest for making requests with a JSON response."""
    forced_params = { 'format': 'json', 'nojsoncallback': 1 }
    response_handler = FlickrJSONResponse
