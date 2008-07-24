"""Contact-related API calls to Flickr."""
from obeattie.photos.flickr.api import base

class GetList(base.FlickrJSONRequest):
    """Get a list of contacts for the calling user."""
    method = 'flickr.contacts.getList'
    optional_params = ['filter', ]
    default_params = { 'filter': 'both', 'page': 1, 'per_page': 1000 }
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 1000 }

class GetPublicList(base.FlickrJSONRequest):
    """Get the 'public' contact list for a user (what's the difference?)."""
    method = 'flickr.contacts.getPublicList'
    optional_params = ['user_id', ]
    required_params = ['user_id', ]
    default_params = { 'page': 1, 'per_page': 1000 }
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 1000 }
