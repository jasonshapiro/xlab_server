# wsgi_app.py
import sys
import os

sys.path.append('/opt/django-projects/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'xlab_server.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()