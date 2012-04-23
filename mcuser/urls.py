from django.conf.urls.defaults import *

urlpatterns = patterns('mcuser.views',
    url(r'^invite/accept/', 'accept_invite'),
    url(r'^invite/', 'invite'),
)