"""URL configuration for the blog application."""
from django.conf.urls.defaults import *

from obeattie.blog import views as blog_views

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>[a-zA-Z]{3})/(?P<day>\d{1,2})/(?P<slug>[\w-]+)/$', blog_views.post_detail, name='post_detail'),
)
