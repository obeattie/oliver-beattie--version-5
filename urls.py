from django.conf.urls.defaults import *
from django.contrib import admin

# Admin autodiscovery
admin.autodiscover()

urlpatterns = patterns('',
    (r'^/?$', 'django.views.generic.simple.direct_to_template', { 'template': 'home.html' }),
    ('^admin/(.*)', admin.site.root),
)
