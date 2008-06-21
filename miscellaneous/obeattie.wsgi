# This file is used to integrade Django and mod_wsgi
# The WSGIHandler() function is used to construct a WSGI application corresponding to our ILP Django app. 

import os, sys

sys.path.extend(['/git-repos/', '/usr/local/', '/Django/Projects/'])
os.environ['DJANGO_SETTINGS_MODULE'] = 'obeattie.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
