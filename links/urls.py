from django.conf.urls.defaults import *

urlpatterns = patterns('obeattie.links.views',
    (r'^quick-add/$', 'quick_add'),
)
