"""Contact-related API calls to Flickr."""
from obeattie.photos.flickr.api import base

class getList(base.FlickrJSONRequest):
    method = 'flickr.contacts.getList'
    valid_params = ['filter', 'page', 'per_page', ]
    default_params = { 'filter': 'both', 'page': 1, 'per_page': 1000 }
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 1000 }

class getPublicList(base.FlickrJSONRequest):
    method = 'flickr.contacts.getPublicList'
    valid_params = ['user_id', 'page', 'per_page', ]
    required_params = ['user_id', ]
    default_params = { 'page': 1, 'per_page': 1000 }
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 1000 }
