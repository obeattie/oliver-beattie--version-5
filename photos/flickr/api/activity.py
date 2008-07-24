"""Activity-related API calls to Flickr."""
from obeattie.photos.flickr.api import base

class userComments(base.FlickrJSONRequest):
    method = 'flickr.activity.userComments'
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 50 }

class userPhotos(base.FlickrJSONRequest):
    method = 'flickr.activity.userPhotos'
    valid_params = ['timeframe', ]
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 50 }
