from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^flickr/', include('obeattie.photos.flickr.urls')),
)