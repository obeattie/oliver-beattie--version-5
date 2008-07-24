"""Activity-related API calls to Flickr. *All of these methods should only be called
   once-per-hour.*"""
from obeattie.photos.flickr.api import base

class UserComments(base.FlickrJSONRequest):
    """Returns a list of recent activity on photos commented on by the calling user.
       *Do not poll this method more than once an hour.*"""
    method = 'flickr.activity.userComments'
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 50 }

class UserPhotos(base.FlickrJSONRequest):
    """Returns a list of recent activity on photos belonging to the calling user.
       *Do not poll this method more than once an hour.*"""
    method = 'flickr.activity.userPhotos'
    optional_params = ['timeframe', ]
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 50 }
