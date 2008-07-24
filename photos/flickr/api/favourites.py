"""Faves-related API calls to Flickr. Note the module is not misspelled; I'm
   British! :P"""
from obeattie.photos.flickr.api import base

class Add(base.FlickrJSONRequest):
    """Adds a photo to a user's favorites list."""
    method = 'flickr.favorites.add'
    required_params = ['photo_id', ]

class GetList(base.FlickrJSONRequest):
    """Returns a list of the user's favorite photos. Only photos which the calling user has permission to see are returned."""
    method = 'flickr.favorites.getList'
    optional_params = ['user_id', 'extras', ]
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 500 }

class GetPublicList(base.FlickrJSONRequest):
    """Returns a list of favorite public photos for the given user."""
    method = 'flickr.favorites.getPublicList'
    required_params = ['user_id', ]
    optional_params = ['extras', ]
    pagination_params = { 'page_key': 'page', 'paginate_by_key': 'per_page', 'max_per_page': 500 }

class Remove(base.FlickrJSONRequest):
    """Removes a photo from a user's favorites list."""
    method = 'flickr.favorites.remove'
    required_params = ['photo_id', ]
