"""Backendy-type Flickrish URLs."""
from django.conf.urls.defaults import *

urlpatterns = patterns('obeattie.photos.flickr.views',
    (r'^authorize/$', 'begin_authorization'),
    (r'^authorize/complete/$', 'complete_authorization'),
)
