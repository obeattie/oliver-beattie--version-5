"""Utilities to help with pagination in the Flickr API."""

class RequestNotPaginatable(Exception):
    """Raised when a request cannot be paginated."""
    pass

class InvalidPage(Exception):
    """Raised when a requested page does not exist."""
    pass

class FlickrAPIPaginator(object):
    """Helps with paginating the Flickr API."""
    def __init__(self, request, max_results=None, *args, **kwargs):
        if not 'page_key' in request.pagination_params and 'paginate_by_key' in request.pagination_params:
            raise RequestNotPaginatable
        self.request = request
        self.paginate_by = self.request.pagination_params.get('max_per_page', 500)
        self.max_results = max_results or self.paginate_by * 10
        self.page_cache = {}
        return super(FlickrAPIPaginator, self).__init__(*args, **kwargs)
    
    @property
    def params(self):
        return self.request.pagination_params
    
    @property
    def max_page(self):
        return (self.paginate_by // self.max_results) or 1
    
    def clone_request(self, altered_params):
        new_params = self.request.params.copy()
        new_params.update(altered_params)
        return self.request.__class__(params=new_params)
    
    def page(self, number):
        if not 1 <= number <= self.max_page:
            raise InvalidPage('Page number out of range.')
        if not number in self.page_cache:
            self.page_cache[number] = self.clone_request({ self.params['paginate_by_key']: self.paginate_by, self.params['page_key']: number })
        return self.page_cache[number]
    
    def __iter__(self):
        """A simple generator of the available pages."""
        current_page = 1
        while current_page <= self.max_page:
            yield self.page(current_page)
            current_page += 1
