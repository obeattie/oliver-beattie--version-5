from django.conf.urls.defaults import *
from django.contrib import admin

# Admin autodiscovery
admin.autodiscover()

urlpatterns = patterns('',
    (r'^/?$', 'django.views.generic.simple.direct_to_template', { 'template': 'home.html' }),
    
    # Includes
    (r'^blog/', include('obeattie.blog.urls')),
    (r'^photos/', include('obeattie.photos.urls')),
    (r'^links/', include('obeattie.links.urls')),
    
    # Django shiz
    ('^admin/(.*)', admin.site.root),
)

# Generic views
urlpatterns += patterns('django.views.generic',
    (r'^(photo|photograph(y|s)?)/(?P<remainder>.*)', 'simple.redirect_to', { 'url': u'/photos/%(remainder)s' }),
    (r'^link/(?P<remainder>.*)', 'simple.redirect_to', { 'url': u'/links/%(remainder)s' }),
)
