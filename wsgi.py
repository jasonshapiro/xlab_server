# wsgi_xlab.py
import site
import os
import sys

SITE_DIR = '/opt/django-trunk/'

site.addsitedir(SITE_DIR) 

sys.path.append(SITE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'xlab_server.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
