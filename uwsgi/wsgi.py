# wsgi_app.py
SITE_DIR = '/opt/django-trunk/xlab_server'
import site
site.addsitedir(SITE_DIR) 

import os
import sys
sys.path.append(SITE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'xlab_server.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
